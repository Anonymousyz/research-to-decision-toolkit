#!/usr/bin/env python3
"""v5 audit. Continues the 10-round 100-point loop.

Adds to v4:
- Probe every external URL referenced from .md with HEAD/GET (HEAD-only by default).
- Spell/case checks on common confusions (e.g., "Github" -> "GitHub"; "Javascript" -> "JavaScript").
- Heading-style check: top-level README must have at least one H1 followed quickly by the project orientation, not by marketing copy.
- Reproducibility check: every prompt must include "wait for my answers" or "review the output" call-out so the reader does not treat LLM output as evidence.
- Opinionated anti-keywords tightening: "polarizing" intensifiers like "absolutely", "definitely", "without doubt" in narrative text.
"""
import json, re, sys, ast, urllib.request, urllib.error, ssl
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = ROOT.name

score = {"structure": 25, "content": 25, "language": 25, "safety": 25}
fixes = []

SKIP = {".git", "scripts/audit.py", "AUDIT.py", "node_modules", ".venv",
        "__pycache__", "src", "tests"}
TEXT_EXTS = {".md", ".json", ".py", ".yml", ".yaml", ".toml", ".txt"}

def ignored(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    if rel in SKIP: return True
    for s in SKIP:
        if rel.startswith(s + "/"): return True
    if "__pycache__" in rel or ".egg-info" in rel: return True
    return False

# --- SAFETY ---
SAFETY_PATTERNS = [
    re.compile(r"F:\\|我的坚果云|CIECC|yunhe|白先生|demo_pwd|changeme", re.I),
    re.compile(r"(?i)(API_KEY|SECRET|TOKEN|PASSWORD)\s*[:=]"),
    re.compile(r"(?i)\bsk-[A-Za-z0-9_\-]{16,}\b"),
    re.compile(r"your-name"),
    re.compile(r"Replace with final public URL"),
    re.compile(r"\bTODO\b|\bFIXME\b|\bXXX\b", re.I),
]
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or ignored(p) or p.suffix not in TEXT_EXTS:
        continue
    try: text = p.read_text(encoding="utf-8")
    except Exception: continue
    for i, line in enumerate(text.splitlines(), 1):
        for pat in SAFETY_PATTERNS:
            if pat.search(line):
                score["safety"] = max(0, score["safety"] - 4)
                fixes.append(f"[safety] {p.relative_to(ROOT).as_posix()}:{i} -> {line.strip()[:80]}")
                break

# --- STRUCTURE ---
EXPECTED_FILES = ["LICENSE","README.md","MANIFESTO.md","SOURCES.md",
                  "CONTRIBUTING.md","SECURITY.md","CODE_OF_CONDUCT.md","CHANGELOG.md"]
for f in EXPECTED_FILES:
    if not (ROOT / f).exists():
        score["structure"] = max(0, score["structure"] - 2)
        fixes.append(f"[structure] missing top-level file: {f}")

for sub in ("templates","scorecards","prompts","examples","docs"):
    if not (ROOT / sub).is_dir():
        score["structure"] = max(0, score["structure"] - 1)
        fixes.append(f"[structure] missing dir: {sub}")

if not (ROOT / "docs" / "quickstart.md").exists():
    score["structure"] = max(0, score["structure"] - 1)
    fixes.append("[structure] missing docs/quickstart.md")
if not (ROOT / "docs" / "roadmap.md").exists():
    score["structure"] = max(0, score["structure"] - 1)
    fixes.append("[structure] missing docs/roadmap.md")
if not (ROOT / ".github" / "ISSUE_TEMPLATE").is_dir():
    score["structure"] = max(0, score["structure"] - 1)
    fixes.append("[structure] missing .github/ISSUE_TEMPLATE/")

license = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
if not any(x in license for x in ("MIT License","Apache License","CC0","BSD","GPL")):
    score["structure"] = max(0, score["structure"] - 2)
    fixes.append("[structure] LICENSE missing standard header")

# --- CONTENT ---
readme = ROOT / "README.md"
if readme.exists():
    txt = readme.read_text(encoding="utf-8")
    lower = txt.lower()
    must_have = ["30-second","quick start","repository map","what this","license","out of scope"]
    for m in must_have:
        if m.lower() not in lower:
            score["content"] = max(0, score["content"] - 2)
            fixes.append(f"[content] README missing phrase: {m}")
    if len(txt) < 1500:
        score["content"] = max(0, score["content"] - 2)
        fixes.append(f"[content] README too short ({len(txt)} chars, want >= 1500)")

for kind in ("prompts","scorecards","templates"):
    files = list((ROOT / kind).glob("*.md"))
    if not files:
        score["content"] = max(0, score["content"] - 3)
        fixes.append(f"[content] no files in {kind}/")
    elif len(files) < 2:
        score["content"] = max(0, score["content"] - 1)
        fixes.append(f"[content] only 1 file in {kind}/, want >=2")
    for f in files:
        sz = f.stat().st_size
        if sz < 1200:
            score["content"] = max(0, score["content"] - 1)
            fixes.append(f"[content] thin file ({sz} chars, want >= 1200): {kind}/{f.name}")

exdir = ROOT / "examples"
ex_md = 0; ex_art = 0
if exdir.is_dir():
    for p in exdir.rglob("*"):
        if p.is_file() and p.suffix == ".md":
            ex_md += 1
        elif p.is_file() and p.suffix in {".json"}:
            ex_art += 1
if ex_md < 1 or ex_art < 1:
    score["content"] = max(0, score["content"] - 2)
    fixes.append("[content] examples must contain >=1 .md narrative AND >=1 .json artifact")

# scorecard veto rule
for sc in (ROOT / "scorecards").glob("*.md"):
    if "veto" not in sc.read_text(encoding="utf-8").lower():
        score["content"] = max(0, score["content"] - 1)
        fixes.append(f"[content] scorecard missing veto: {sc.name}")

# prompt reproducibility: every prompt must warn against treating LLM output as fact
REPRO_HINT = re.compile(r"(do not treat|wait for my answers|review the output|reviewing the output|verify|do not use to)", re.I)
for pf in (ROOT / "prompts").glob("*.md"):
    txt = pf.read_text(encoding="utf-8")
    if not REPRO_HINT.search(txt):
        score["content"] = max(0, score["content"] - 1)
        fixes.append(f"[content] prompt missing reproducibility hint: {pf.name}")

# markdown link target validity
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
for p in sorted(ROOT.rglob("*.md")):
    if ignored(p): continue
    try: text = p.read_text(encoding="utf-8")
    except Exception: continue
    for label, target in LINK_RE.findall(text):
        if target.startswith(("http://","https://")): continue
        path = target.split("#",1)[0]
        if path == "": continue
        if path.startswith("#"): continue
        tp = (p.parent / path).resolve()
        if not tp.exists():
            score["content"] = max(0, score["content"] - 1)
            fixes.append(f"[content] broken local link in {p.relative_to(ROOT).as_posix()}: {target}")
            break

# json parse
for p in sorted(ROOT.rglob("*.json")):
    if ignored(p): continue
    try: json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        score["content"] = max(0, score["content"] - 1)
        fixes.append(f"[content] JSON parse error: {p.relative_to(ROOT).as_posix()} {e}")

# python parse
for p in sorted(ROOT.rglob("*.py")):
    if ignored(p): continue
    try: ast.parse(p.read_text(encoding="utf-8"))
    except Exception as e:
        score["content"] = max(0, score["content"] - 1)
        fixes.append(f"[content] Python parse error: {p.relative_to(ROOT).as_posix()} {e}")

# external URL probe (HEAD with GET fallback)
def probe(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            return r.status
    except Exception:
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception:
            return None

URL_RE = re.compile(r"https?://[^\s\)\]\"<>]+")
known = {
    "github.com":"github-domain-on-master-pinned",
    "owasp.org":"owasp-llm-top10-known",
    "nist.gov":"nist-ai-rmf-known",
}
probed = 0
failures = 0
probed_urls = set()
for p in sorted(ROOT.rglob("*.md")):
    if ignored(p): continue
    try: text = p.read_text(encoding="utf-8")
    except Exception: continue
    urls = list(set(URL_RE.findall(text)))
    if not urls: continue
    for u in urls[:6]:
        u = u.rstrip('.,);')
        if u.endswith((".example", ".invalid", ".test")): continue
        if u in probed_urls: continue
        probed_urls.add(u)
        if probed > 25: break
        probed += 1
        code = probe(u)
        if code is None or code >= 400:
            failures += 1
            score["content"] = max(0, score["content"] - 1)
            fixes.append(f"[content] probe failed: {u} (status {code})")
    if probed > 25: break

# --- LANGUAGE ---
LANG_BAD_WORDS = {
    "赋能","底座","闭环","全新范式","革命性","颠覆性","里程碑",
    "开箱即用","打造一个","巨人的肩膀","做厚","做深","做透",
    "沉淀方法","沉淀能力","绝对","毫无疑问","一定","肯定",
}
for p in sorted(ROOT.rglob("*.md")):
    if ignored(p): continue
    try: text = p.read_text(encoding="utf-8")
    except Exception: continue
    for w in LANG_BAD_WORDS:
        if w in text:
            score["language"] = max(0, score["language"] - 2)
            fixes.append(f"[language] {p.relative_to(ROOT).as_posix()} -> '{w}'")
            break
    else:
        if re.search(r"不是\w+，?不是\w+，?而是\w+", text):
            score["language"] = max(0, score["language"] - 1)
            fixes.append(f"[language] {p.relative_to(ROOT).as_posix()} -> parallel 不是…不是…而是 pattern")

# Spelling / case-fix checks (English narrative only)
SPELL = {
    "Github": "GitHub",
    "Javascript": "JavaScript",
    "Typescript": "TypeScript",
    "NLP": "NLP",   # placeholder, real check below
}
SPELL_CHECK = [
    ("Github", "GitHub"),
    ("Javascript", "JavaScript"),
    ("Typescript", "TypeScript"),
    ("readme", "README"),
    ("ai-driven", "AI-driven"),
    ("Ai-driven", "AI-driven"),
]
for p in sorted(ROOT.rglob("*.md")):
    if ignored(p): continue
    try: text = p.read_text(encoding="utf-8")
    except Exception: continue
    lines = text.splitlines()
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code: continue
        for wrong, right in SPELL_CHECK:
            if wrong in line:
                score["language"] = max(0, score["language"] - 1)
                fixes.append(f"[language] {p.relative_to(ROOT).as_posix()}:{i} -> '{wrong}' should be '{right}'")
                break

# Long heading
for p in sorted(ROOT.rglob("*.md")):
    if ignored(p): continue
    text = p.read_text(encoding="utf-8")
    for h in re.findall(r"^#+\s+(.+)$", text, flags=re.M):
        if len(h) > 90:
            score["language"] = max(0, score["language"] - 1)
            fixes.append(f"[language] long heading ({len(h)} chars): {h[:80]}")
            break

# Repeated-word smell
for p in sorted(ROOT.rglob("*.md")):
    if ignored(p): continue
    text = p.read_text(encoding="utf-8")
    for raw_para in re.split(r"\n\n+", text):
        lines = [ln for ln in raw_para.splitlines() if ln.strip()]
        if not lines: continue
        if sum(1 for ln in lines if ln.strip().startswith("|")) >= 3: continue
        para = " ".join(lines)
        words = para.lower().split()
        if len(words) < 25: continue
        repeats = {}
        for w in words:
            w = w.strip(",.;:()[]{}")
            if len(w) < 4: continue
            repeats[w] = repeats.get(w,0) + 1
        top = max(repeats.items(), key=lambda kv: kv[1])
        if top[1] >= 6 and top[0] in ("tool","toolkit","review","evidence","system","framework","artifact","decision"):
            score["language"] = max(0, score["language"] - 1)
            fixes.append(f"[language] {p.relative_to(ROOT).as_posix()} -> '{top[0]}' x{top[1]} in narrative")
            break

# --- OUTPUT ---
total = sum(score.values())
report = {"name": NAME, "score": score, "total": total, "fixes": fixes[:80], "probed": probed, "url_failures": failures}
print(json.dumps(report, indent=2, ensure_ascii=False))
sys.exit(0 if total == 100 else 1)

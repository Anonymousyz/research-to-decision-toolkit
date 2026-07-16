# Judgment Writing Module

Judgment writing treats expression as the last quality gate, not the first:

```text
research sufficiency → claim strength → evidence fit → structure → wording → delivery
```

The module is an author-designed synthesis for research, policy, governance, and product-decision artifacts. It is **not** a universal writing theory, automatic quality score, or permission to overstate a conclusion.

## Two paths

- **Path A — write now:** the decision, audience, evidence, and claim boundary are clear enough to draft, review, and deliver.
- **Path B — return to research:** an important claim still lacks evidence, a competing explanation remains unresolved, or the action boundary cannot yet be stated. Gather evidence or downgrade the claim before drafting.

`writing_review.path` records the **current disposition at review completion**, not an immutable history flag. If Path B work is completed and the packet is then supportable, the final reviewed record should use Path A; the five pass findings preserve what was corrected.

Choosing Path B is not failure. It prevents polished prose from hiding weak cognition or evidence.

## Five ordered passes

1. **Judgment** — Is the conclusion stronger than the available evidence?
2. **Evidence** — Can each material claim be traced, challenged, and revised?
3. **Structure** — Does the sequence move from problem to inference to action?
4. **Clarity** — Are key terms, sentences, and transitions unambiguous for the intended reader?
5. **Delivery** — Will the artifact survive the author, reach the reader, and generate reviewable feedback?

The passes are ordered because later editing must not disguise an earlier failure. Do not begin with tone polishing when the real defect is unsupported judgment.

## Human responsibility

`reviewed_by`, `reviewed_at`, and `review_method` expose who accepted the final artifact. AI may suggest edits, but it is not an independent reviewer, source, decision owner, or circulation authority. Permission and confidentiality checks remain human responsibilities.

## Manual template

Use [`templates/five-pass-writing-review.md`](templates/five-pass-writing-review.md). The v0.6 JSON schema records each pass as a `finding` and a `revision`; it does not assign a writing-quality score.

## Failure modes

- treating fixed word counts or reading-time rules as universal laws;
- using source quantity as a proxy for source sufficiency;
- polishing language before resolving the decision;
- compressing uncertainty into false confidence;
- anonymizing material without obtaining publication permission;
- claiming the artifact is effective before reader feedback exists.

The canonical 24-point decision-readiness score remains unchanged. The writing review is a traceable process record, not a calibrated measure of literary or policy quality.

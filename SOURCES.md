# Sources and influence map

This toolkit combines ideas from decision analysis, pre-mortem review, open/reproducible research, public-policy appraisal, and AI risk management. The 24-point scoring thresholds and repository workflow are **author-designed and uncalibrated**; the sources below inform individual practices but do not validate this implementation.

## Primary and authoritative sources

| Source | Public URL | Practice used here | Boundary |
|---|---|---|---|
| Gary Klein, PreMortem method | https://www.gary-klein.com/premortem | Imagine failure before commitment and work backward to causes | Does not prescribe this repository's score |
| NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | Connect context, measurement, governance, and risk treatment | Voluntary framework; not certification |
| NIST AI RMF Playbook | https://airc.nist.gov/airmf-resources/playbook/ | Evidence-oriented actions across Govern, Map, Measure, Manage | Suggested actions require local tailoring |
| OWASP GenAI Security Project | https://genai.owasp.org/ | Security challenge categories for AI-enabled decisions and systems | Threat guidance is not a control-effectiveness opinion |
| The Turing Way | https://book.the-turing-way.org/ | Reproducible, ethical, collaborative, and communicable research practices | Research handbook, not decision authorization |
| Center for Open Science | https://www.cos.io/ | Transparency, preregistration, and explicit analysis plans | Scientific workflow patterns need adaptation for policy/business use |
| UK HM Treasury Green Book | https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government | Options, appraisal, uncertainty, and evaluation thinking | UK public-sector guidance; not universally binding |
| UK HM Treasury Magenta Book | https://www.gov.uk/government/publications/the-magenta-book | Evaluation design and evidence-use discipline | Evaluation guidance; does not validate this scorecard |

## Books and secondary influences

- Chip Heath and Dan Heath, *Decisive* — widening options, reality-testing assumptions, and preparing to be wrong.
- Annie Duke, *Thinking in Bets* — separating decision quality from outcome quality.
- Barbara Minto, *The Pyramid Principle* — decision-oriented structuring and communication.
- Colin Bryar and Bill Carr, *Working Backwards* — artifact-first clarification of customer value and decisions.

Books are listed as influences rather than copied templates. Users should consult the original editions for exact claims.

## Original contribution

The repository's contribution is the integration of:

```text
research framing → structured claims → source tiers → decision brief → artifact plan → feedback loop → red-team review
```

No cited source endorses the 24-point scale, thresholds, or veto list. See [`docs/method_status.md`](docs/method_status.md).

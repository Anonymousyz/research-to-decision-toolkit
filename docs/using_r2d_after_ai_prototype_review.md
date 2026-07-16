# Using Research-to-Decision after an AI prototype review

The [AI Prototype-to-Production Toolkit](https://github.com/Anonymousyz/ai-prototype-to-production-toolkit) asks whether an AI system has the evidence and controls needed to move beyond a demo. This toolkit is useful when the answer has to become a decision packet for accountable humans.

The two tools do different jobs:

| Question | Use | Output |
|---|---|---|
| Does the prototype have a defined workflow, data boundary, evaluation plan, owner, logs, and rollback path? | Prototype-to-Production Toolkit | Fixed 70-point structural readiness assessment and veto list |
| Should the organization proceed, pause, narrow scope, or choose another path? | Research-to-Decision Toolkit | Decision packet with evidence, alternatives, criteria, stakeholders, trade-offs, reversibility, and pre-mortem failure |
| Which evaluation, observability, guardrail, or governance component might close a gap? | [Awesome AI Production Readiness](https://github.com/Anonymousyz/awesome-ai-production-readiness) | Curated tool and standards map |

## A fictional operating path

1. A team proposes an AI assistant for one bounded workflow.
2. The readiness assessment identifies the evidence that exists, the gaps that remain, and any veto condition.
3. If a material decision is required, the decision owner opens a R2D brief.
4. The brief records at least two alternatives. “Proceed with a controlled pilot” is one option, not the default answer.
5. The team names acceptance criteria, affected stakeholders, operating owner, stop condition, and feedback route.
6. An accountable human decides whether to proceed, revise, defer, or decline.

Neither CLI passes an assessment automatically to the other. The handoff is deliberate because the decision owner must interpret the evidence, rather than treat a score as authorization.

## What to carry into the decision packet

- the workflow being changed;
- authorized and prohibited data;
- evaluation results and their limits;
- unresolved vetoes and top gaps;
- human review and override design;
- rollback condition and operating owner;
- plausible alternatives, including a narrower pilot or no deployment;
- evidence that would change the conclusion.

## Example commands

```bash
# First: validate a readiness assessment in the flagship toolkit
ai-ready validate examples/sample_assessment.json

# Then: validate and score a separate decision packet here
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
r2d score examples/fictional-ai-governance-research-to-decision/decision_brief.json
```

The examples are fictional. A successful command confirms JSON structure and declared conditions. It does not verify the source material, authenticate a reviewer, or approve a real deployment.

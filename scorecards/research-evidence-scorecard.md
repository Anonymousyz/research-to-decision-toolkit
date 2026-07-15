# Research evidence scorecard

A second, evidence-deep scorecard for the same brief. Use this when the team disagrees about which facts and which assumptions matter.

## Per-evidence scoring (0-2 each)

| # | Claim | Strength of source | Independence | Recency | Action |
|---|---|---|---|---|---|
| 1 | _claim_ | _official/peer/public blog_ | _independent? y/n_ | _date_ | _add / drop / harden_ |
| 2 | | | | | |

## Coverage checks

- at least one fact per major claim
- at least one source per assumption
- at least one counter-source per major claim

## Reverse-score

If the brief claims a low-risk decision but the reverse-score is high, the brief is incomplete. The reverse-score is the count of high-impact surprises if the recommended option is wrong.

| Surprising outcome | Pre-mortem covered it? |
|---|---|
| | |

## Veto items

- every claim is an assumption and no source is named;
- the reverse-score is above 5 with no mitigation;
- the brief claims a low-risk decision while assuming more than 70% accuracy on a self-built eval.

## Output

- Strength: __ / 24
- Reverse-score: __ / 8
- Action: more evidence / ship as-is / defer

## Worked example

> Claim 1 (fact): "OWASP LLM Top 10 lists prompt injection as LLM01."
> Source: owasp.org.
> Score: strength 2, independence 2, recency 1.

> Claim 2 (assumption): "Our retrieved context hits >95% of the user-asked questions."
> Source: internal pilot with 30 cases.
> Score: strength 1, action: harden.

## Reverse-score worked example

> Surprising outcome: a regulated customer redacts the copilot's output in 60% of cases.
> Pre-mortem covered? Partly.

## Notes

The reverse-score penalizes briefs that claim a low-risk decision while omitting obvious surprises.

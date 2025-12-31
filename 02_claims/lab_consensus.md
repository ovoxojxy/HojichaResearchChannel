# Lab Consensus (Current)

## Current extension focus (v0)
1. **Cross-turn information retention patterns** (primary)
2. **Proactive information gathering** (secondary; operationalization contested)

## Strongest accepted critiques / risks
- Correlation ≠ causation risk: success-correlated behaviors are not automatically causal drivers.
- Taxonomy completeness risk: human-derived categories may miss model-native behaviors.
- Linguistic markers can be stylistic rather than functional.
- Scaffolding can induce scaffold-dependence and mask limitations.
- Tool-using agents create multi-stream state; single-stream diagnostics can fail.

## Working hypothesis
- As tasks become less structured / more open-ended, success depends on behaviors that models do not reliably deploy unless guided.
- Guidance helps capable models but harms smaller ones, suggesting a capability threshold / instruction-load interaction.

## What we’re trying to measure next
- Retention: constraint stability, entity/value drift, correct reuse across turns (explicit or implicit).
- Proactive gathering: temporal/tool-call patterns that predict downstream coherence/success.
- Linguistic vs structural measurement mismatch: where each succeeds or fails.

## Fast falsifiers (near-term)
- Retention markers show no association with success (including when measured without relying on explicit “as mentioned earlier” phrasing).
- Structural trajectory features provide no incremental predictive value over baseline accuracy/correctness and simple length controls.
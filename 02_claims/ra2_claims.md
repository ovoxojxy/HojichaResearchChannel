# RA2 — Claims & Contributions

## Key claims
- [C1] **Capacity-dependent degradation**: smaller models degrade when explicitly scaffolded with cognitive behaviors, while larger models benefit — suggests an architectural constraint / capability threshold.
- [C2] Fragile assumption: the cognitive taxonomy may be **incomplete** because it is human-derived and may miss model-specific behaviors that don’t map to human cognitive structures.

## Critiques of other claims
- [X1] RA1 “under-utilization” claim is weaker than it sounds: it assumes **causation from correlation**.
  - Alternative: models may succeed through strategies not captured by the taxonomy.
  - Another possibility: systematic patterns reflect annotation framework bias rather than genuine behavioral gaps.

## Compatibility with RA3
- [C3] Partial compatibility with tension:
  - If smaller models can’t coordinate elements, “under-utilization” may be a capacity limitation.
  - But if taxonomy misses what matters, then “under-utilization” might be an artifact.

## Operationalization stance
- [O1] **Proactive information gathering** is hardest to operationalize: it may require inferring anticipatory intent (subjective).
- [O2] **Cross-turn retention** is more feasible: explicit linguistic markers are extractable; can be high agreement; can be partially automated.

## Falsification / invalidation condition
- [F1] If explicit cross-turn references do **not** correlate with success in multi-turn agentic settings, then the retention extension may be stylistic rather than functional.

## Related paper
- [P1] “Revisiting Uncertainty Estimation and Calibration of Large Language Models” (arXiv:2505.23854) uses linguistic markers for calibration; relevant as a “linguistic signal” case study but distinct from retention.

## Methodological fragility (paper critique)
- [M1] Self-consistency: agreement across reasoning paths ≠ correctness; conflates consistency with verification.

## Open questions / uncertainties
- [Q1] How to separate functional retention from stylistic “reference language”?
- [Q2] How to design measures that don’t just reward verbosity or superficial linking?
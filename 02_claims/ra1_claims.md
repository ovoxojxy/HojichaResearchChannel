# RA1 — Claims & Contributions

## Key claims
- [C1] Models **under-utilize cognitive elements correlated with success**, especially on ill-structured problems (strongest framing from the Cognitive Foundations paper analysis).
- [C2] A major fragile assumption in the paper: **behavioral markers are treated as comparable across humans and LLMs** without establishing process-level equivalence.

## Proposed extension(s)
- [E1] **Cross-turn information retention patterns** as the first “beyond reasoning” behavior family:
  - Motivations: addresses a gap in multi-turn settings; more observable than proactive gathering; stronger cognitive science grounding; captures distinct failure modes (information access vs goal persistence).

## Methodology critiques
- [M1] RA2’s uncertainty-calibration direction is methodologically fragile if it infers internal confidence from linguistic markers without establishing the link.
- [M2] RA3’s agentic systems direction highlights a mismatch: structural signals vs linguistic observables; it exposes measurement differences more than it directly supports the core extension.

## Proposed diagnostics / measurements
- [D1] Use **explicit reference frequency over turns** as a diagnostic to distinguish:
  - capacity limits: decreasing references + increasing incoherence
  - strategy misalignment: references maintained + coherent but wrong
- [D2] Note limitation: tool-using agents have multi-stream state, so a single-stream “reference count” diagnostic can fail without extensions.

## Related work notes
- [P1] Wang et al. (2022) self-consistency operationalizes “verification” but misses:
  - false consistency (consistently wrong)
  - inability to detect genuine error checking vs spurious agreement

## Open questions / uncertainties
- [Q1] How to measure retention robustly when models reuse context implicitly (without explicit references)?
- [Q2] How to generalize diagnostics to tool-using settings with multiple information streams?
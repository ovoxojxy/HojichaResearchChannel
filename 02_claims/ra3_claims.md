# RA3 — Claims & Contributions

## Key claims
- [C1] Under-emphasized claim from the paper: **capacity-dependent reversal** — smaller models (7B–8B) degrade with explicit scaffolding while larger models (30B+) benefit; suggests these behaviors may be capacity-emergent rather than easily trainable.
- [C2] Unacknowledged risk: test-time reasoning guidance can create **scaffold-dependent** behavior and mask architectural limitations.

## Proposed extension(s)
- [E1] **Cross-turn information retention patterns**
  - Observable via explicit linguistic markers (“as mentioned earlier…”) and consistency of constraints/values.
  - Importance: predicts trajectory coherence in agentic settings; conversational coherence in interactive settings.
- [E2] **Proactive information gathering**
  - Tool calls or questions that seek information before it is needed.
  - Observable via temporal patterns (gap between retrieval and use), future-oriented language, parallel tool calls.

## Defense / operationalization argument
- [O1] Proactive gathering can be operationalized without pure “intent inference” by relying on measurable temporal/tool-call patterns.

## Critiques / limitations
- [L1] RA1 diagnostic fails for tool-using agents because agents have multiple information streams (conversation, tool outputs, environment state). Single-stream reference counting can miss coordination failures.

## Related work
- [P1] “An Approach to Checking Correctness for Agentic Systems” (Sheffler, arXiv:2509.20364): emphasizes **structural** signals (tool call sequences, state transitions, inter-agent comms), implying structural signals may complement linguistic ones.

## Deployment risk highlighted
- [R1] Linguistic uncertainty marker transfer can fail in deployment due to domain transfer, suppression, and style vs function — risks breaking calibration-based safety mechanisms.

## Open questions / uncertainties
- [Q1] What’s the best combined measurement suite: linguistic + structural?
- [Q2] How to prevent scaffolding from becoming a crutch rather than enabling general capability?
# Project Scope

## Goal
Extend the Cognitive Foundations paper by expanding analysis beyond “reasoning elements” into additional behavior families that matter in multi-turn and agentic trajectories (e.g., cross-turn information retention, proactive information gathering), and evaluate whether these behaviors predict success, robustness, and calibration across model families and capacities.

## Primary research questions
1. **Beyond reasoning elements:** What additional behavior families (especially in multi-turn / agentic settings) are strongly associated with success or failure?
2. **Observability + instrumentation:** What can be measured reliably using linguistic signals vs structural trajectory signals (tool calls, state transitions), and where do these diverge?
3. **Capacity thresholds:** When does explicit scaffolding help vs harm, and does this reflect a capability threshold or an instruction-load effect?
4. **Process validity:** When do behavioral markers reflect meaningful underlying processes vs post-hoc rationalization or stylistic artifacts?

## Initial candidate extensions (v0)
- **Cross-turn information retention patterns** (primary focus): information persistence, constraint stability, entity/value drift, correct reuse across turns.
- **Proactive information gathering** (secondary focus): “ahead of need” questions/tool calls; temporal patterns between retrieval and use; parallel tool calls.

## Working hypotheses
- Models may **under-deploy behaviors correlated with success** on ill-structured or open-ended problems (but correlation≠causation is a known risk).
- **Explicit structural scaffolding** improves performance for capable models but can degrade smaller models (suggesting a **capability threshold** / architecture constraint).
- Purely **linguistic markers** can be non-functional style; **structural signals** may capture complementary failure modes in tool-using agents.

## Known risks / fragile assumptions
- Behavioral markers may not correspond to the same cognitive processes in humans vs models (process-level equivalence not established).
- Taxonomy completeness risk: model-specific behaviors may not map cleanly to human-derived cognitive foundations.
- “Success correlation” may reflect annotation framework bias or confounds rather than causal drivers.
- Scaffolding can induce **scaffold-dependence**, masking architectural limitations instead of improving underlying capability.

## Non-goals (for now)
- Claims about internal cognition without process validation.
- Domain-specific applications unrelated to the benchmark/research goal.
- Productionizing agents (this is measurement + research instrumentation).

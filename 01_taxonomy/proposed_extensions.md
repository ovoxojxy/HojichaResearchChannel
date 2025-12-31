# Proposed Behavior Extensions (Beyond Reasoning Elements)

## B1: Cross-turn information retention patterns (Primary)

### Definition
Ability to preserve, retrieve, and correctly reuse relevant information (constraints, entities, values, decisions) from earlier turns across multi-turn interactions.

### Why this matters
- Multi-turn/agentic settings depend on trajectory coherence.
- Captures a gap between goal maintenance and information access.
- Potentially more observable and annotatable than proactive gathering.

### Observables (linguistic + functional)
- Correct reuse of previously stated constraints/values (even without explicit “as mentioned…” language)
- Stable entity references and consistent commitments
- Minimal drift after tool outputs or long contexts

### Failure modes
- Constraint loss or overwrite after new info/tool outputs
- Entity/value drift (subtle substitutions)
- Confabulated continuity (“remembering” facts never stated)
- Incoherent re-derivation loops / repetitive verification with no learning

### Measurement candidates (v0)
- Constraint consistency score across turns
- Entity/value drift rate
- Reference correctness (not just frequency)
- “State overwrite” events after tool outputs (if applicable)

### Falsification risk
If retention metrics do not correlate with success (and do not improve under controlled prompting), then the behavior may be stylistic or non-functional.

---

## B2: Proactive information gathering (Secondary; contested)

### Definition
Seeking information (questions/tool calls) before it is explicitly required, enabling future steps and reducing downstream uncertainty.

### Observables (proposed)
- Temporal gap: info acquired earlier than its usage
- Future-oriented language indicating planning horizon
- Parallel tool calls with different time horizons / information needs
- Retrieval diversity: multiple sources queried before committing

### Measurement candidates (v0)
- “Acquire-to-use” lag (time/turn distance)
- Tool-call timing relative to decision points
- Breadth of sources/tools prior to commitment

### Known risks
- Intent inference may be subjective; need measurable anchors
- Could be confounded with verbosity or over-searching
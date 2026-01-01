# Spec Freeze v0.1 — Cross-Turn Information Retention

**Status:** Frozen for Pilot  
**Date:** 2026-01-01  
**Owner:** PI (Jarod)

This document freezes the task, behavior definition, and evaluation assumptions for the pilot annotation round (v0.1). No changes should be made during the pilot.

---

## 1. Behavior Under Study

**Cross-Turn Information Retention**  
A model’s ability to maintain and correctly apply necessary information across non-adjacent turns in multi-step interactions involving conversation, tools, and environment state.

This is evaluated strictly through **observable outcomes**, not inferred intent or internal reasoning.

---

## 2. Task Definition (Frozen)

**Task:** Deferred Configuration Validation

**Turn Structure:**
1. Conversation: user provides configuration value (rate limit = 100)
2. Tool: system is configured via `set_rate_limit`
3. Tool (distractor): unrelated system query
4. Tool: implicit validation via `validate_config`

**Key property:**  
Validation depends on information from Turns 1 and 2 after an intervening distractor, preventing adjacency-based solutions.

---

## 3. Task-Grounded Necessary Information

The following information is defined as *necessary* independently of model behavior:

- Target configuration value from conversation (Turn 1)
- Configuration result from tool output (Turn 2)
- Environment state consistency at validation time

If a trajectory’s outcome indicates failure to use this information, a retention failure is inferred.

---

## 4. Retention Levels (Outcome-Based)

### Level 0 — Information Loss
Observable indicators:
- Missing required parameters at validation
- Re-querying information already obtained
- Task failure attributable to missing prior information

### Level 1 — Retained but Misapplied
Observable indicators:
- No re-queries
- Correct information appears available
- Task fails due to incorrect application (e.g., wrong comparison logic)
- Or success achieved using only a single stream (no evidence of cross-stream coordination)

### Level 2 — Coherent Multi-Stream Coordination
Observable indicators:
- Task succeeds
- No unnecessary re-queries
- No error patterns
- Correct validation outcome consistent with task structure

---

## 5. Evaluation Assumptions

### Full Observability Condition
Available:
- Tool call sequence
- Tool parameters and outputs
- Error messages
- Final task outcome

### Partial Observability Condition
Available:
- Tool call sequence (names only)
- Error types
- Final task outcome

Unavailable:
- Conversation content
- Tool outputs
- Parameter values

Ambiguity under partial observability is expected and should be recorded.

---

## 6. Pilot Goals

This pilot is intended to test:
- Whether the rubric can be applied consistently by a blind annotator
- Where outcome-based signals suffice vs. break
- Which ambiguities are fundamental vs. logging artifacts

No new behaviors, tasks, or metrics should be introduced during the pilot.

---

## 7. Change Policy

Any revisions to:
- retention definitions
- level boundaries
- task structure
must wait until **after** pilot_v0.1 reconciliation.
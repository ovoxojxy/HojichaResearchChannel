# Deployment Robustness Under Partial Observability

The deferred rate-limit validation task remains diagnostic under deployment constraints where conversation history and tool outputs are hidden or sanitized. This robustness stems from the task's structure, which defines necessary dependencies independently of observable traces, allowing retention failures to be inferred from action outcomes rather than direct information tracking.

## Signals That Remain Observable

When conversation history and tool outputs are hidden or sanitized, the following signals remain observable from execution traces and error logs:

### 1. Tool Call Sequences

The sequence of tool invocations (`set_rate_limit` → `get_system_status` → `validate_config`) is observable from execution logs independent of tool output content. Re-query patterns—where Turn 4 calls `get_current_limit()` again instead of using Turn 2's result, or where `set_rate_limit()` is called repeatedly—are detectable from call sequence logs even when tool outputs are sanitized.

**Example**: If Turn 4 calls `get_current_limit()` after Turn 2 already returned `current_limit: 100`, this re-query pattern is observable from the tool call sequence log, indicating retention failure without requiring visibility into Turn 2's output content.

### 2. Task Completion Outcomes

Final task success or failure is observable from system outcomes (validation results, API response codes, error absence). If Turn 4 fails because it uses an incorrect rate limit parameter (when task structure requires using the rate limit value from Turn 1 and configuration status from Turn 2), retention failure is inferred from task outcome.

**Example**: If Turn 4's `validate_config()` call fails with `{"valid": false, "message": "missing required parameter: limit"}`, this outcome is observable from the validation result, indicating retention failure without requiring visibility into Turn 1's conversation or Turn 2's tool output.

### 3. Error Patterns

Errors indicating missing prior information are observable from error logs without requiring tool output visibility. If Turn 4 produces errors that would not occur if prior information were retained, retention failure is inferred.

**Specific error patterns for deferred rate-limit validation:**
- **Missing limit parameter**: Turn 4 calls `validate_config()` without the rate limit parameter, producing error `"missing required parameter: limit"`. This error is observable from validation response logs, indicating that Turn 1's rate limit value (100) was not retained.
- **Validation mismatch**: Turn 4 calls `validate_config(limit=?)` with incorrect value, producing error `"limit mismatch"`. This error is observable from validation response logs, indicating that either Turn 1's target value or Turn 2's configured value was not retained correctly.
- **Repeated configuration**: Turn 4 calls `set_rate_limit()` again instead of validating, or calls `set_rate_limit()` multiple times. This pattern is observable from tool call sequence logs, indicating retention failure.

### 4. Efficiency Degradation

Unnecessary re-queries are observable from tool call frequency patterns even when outputs are sanitized. Redundant tool invocations are detectable from execution traces.

**Specific efficiency signals for deferred rate-limit validation:**
- **Re-query pattern**: Turn 4 calls `get_current_limit()` when the limit was already returned in Turn 2's `set_rate_limit()` output. This is observable from API call logs showing `get_current_limit()` called after `set_rate_limit()`, indicating information loss.
- **Repeated configuration**: Turn 4 calls `set_rate_limit()` again instead of validating, or multiple `set_rate_limit()` calls occur. This is observable from execution traces, indicating retention failure or confusion about task state.

## How Outcome-Based Indicators Remain Diagnostic

The task structure defines necessary dependencies independently: Turn 4 requires the rate limit value (100) from Turn 1 (conversation stream) and the configuration status from Turn 2 (tool output stream). Retention failures manifest as observable consequences:

### Task Completion Patterns

If Turn 4 fails when task structure requires using the rate limit value from Turn 1 and configuration status from Turn 2, retention failure is inferred from task outcome. This works because:
- Task success/failure is observable from validation results (`{"valid": true}` vs. `{"valid": false}`)
- Dependencies are defined by task structure (Turn 4 must validate using information from Turns 1 and 2), not by examining tool outputs
- Validation outcomes are observable even when conversation history and tool outputs are hidden

**Example**: Turn 4's validation returns `{"valid": false, "message": "missing required parameter: limit"}`. This outcome indicates retention failure (Turn 1's rate limit value was not retained) without requiring visibility into Turn 1's conversation or Turn 2's tool output.

### Error Patterns

Errors indicating wrong parameter usage or missing information are observable from error logs. If Turn 4 produces errors that indicate using incorrect rate limit value when correct one was obtained earlier, retention failure is inferred without seeing tool outputs.

**Example**: Turn 4 calls `validate_config(limit=50)` when the correct value is 100, producing error `"limit mismatch"`. This error pattern is observable from validation response logs, indicating retention failure without requiring visibility into Turn 1's conversation or Turn 2's tool output.

### Re-Query Patterns

If Turn 4 calls `get_current_limit()` again instead of using Turn 2's result, this is observable from tool call sequence logs. The efficiency signal (unnecessary re-queries) remains diagnostic even when tool outputs are sanitized.

**Example**: Tool call sequence log shows: Turn 2: `set_rate_limit(limit=100)`, Turn 3: `get_system_status()`, Turn 4: `get_current_limit()`. The re-query pattern (Turn 4 calling `get_current_limit()` after Turn 2 already returned the limit) is observable from the sequence log, indicating retention failure without requiring visibility into Turn 2's output content.

### Efficiency Signals

Redundant tool invocations are observable from execution traces. State inconsistencies requiring correction are observable from state change logs, even without full state visibility.

**Example**: Execution trace shows multiple `set_rate_limit()` calls (Turn 2 and again in Turn 4), indicating confusion about task state or retention failure. This pattern is observable from execution traces without requiring tool output visibility.

## Signals That Fail Under Partial Observability

The following signals fail when conversation history and tool outputs are hidden:

1. **Direct parameter matching**: Checking whether Turn 4's `validate_config(limit=?)` parameter matches Turn 1's rate limit value (100) or Turn 2's `current_limit` value requires unsanitized tool outputs and conversation history. This structural diagnostic is not available under partial observability.

2. **Semantic consistency measurements**: Comparing semantic similarity between Turn 4's validation response and prior context (Turn 1's rate limit request, Turn 2's configuration status) requires full conversation history and tool output visibility.

3. **Tool-conversation integration patterns**: Detecting whether agents integrate Turn 1's conversation input (rate limit request) with Turn 2's tool output (configuration status) requires visibility into both streams.

4. **Configuration status tracking**: Directly verifying whether Turn 4 uses Turn 2's `status: "configured"` or `current_limit: 100` values requires unsanitized tool outputs.

## Why This Does Not Break the Evaluation

The evaluation remains diagnostic because retention failures manifest as observable action outcomes. The task structure defines necessary dependencies independently (Turn 4 needs rate limit value from Turn 1 and configuration status from Turn 2), so failures produce detectable consequences:

- **Task failures when dependencies aren't met**: Turn 4's validation fails with `{"valid": false, "message": "missing required parameter: limit"}` or `"limit mismatch"` when required information is not retained
- **Error patterns indicating missing prior information**: Validation errors (missing parameter, mismatch) are observable from error logs
- **Re-query patterns showing information loss**: `get_current_limit()` called after `set_rate_limit()` already returned the limit, observable from call sequence logs
- **Efficiency degradation from redundant operations**: Multiple `set_rate_limit()` calls or unnecessary `get_current_limit()` calls, observable from execution traces

These outcome-based indicators are sufficient to detect retention failures without requiring direct parameter matching or semantic analysis. The evaluation trades direct structural verification (parameter matching between turns) for indirect outcome-based inference (task failures, errors, re-queries), which is more robust to deployment constraints while remaining diagnostic.

## Deployment Scenarios

This robustness enables evaluation in production settings where:
- Tool outputs are sanitized for security/privacy (e.g., `set_rate_limit()` output with `current_limit: 100` is redacted)
- Conversation history is truncated or not fully accessible (e.g., Turn 1's rate limit request is not available)
- Only final outcomes and error logs are available (e.g., validation results and error messages are logged, but intermediate tool outputs are not)
- Execution traces are logged but content is redacted (e.g., tool call sequences are logged, but parameters and return values are sanitized)

The deferred rate-limit validation task demonstrates that retention evaluation can remain diagnostic under partial observability when task structure defines dependencies independently and retention failures produce observable consequences (validation failures, error patterns, re-query sequences, efficiency degradation).



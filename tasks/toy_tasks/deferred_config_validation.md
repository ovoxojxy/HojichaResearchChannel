 # Toy Task: Deferred Configuration Validation

We design a minimal four-turn task that requires cross-turn information retention across conversation, tool outputs, and environment state, with an intervening distractor step that prevents solutions based on adjacency or immediate parameter passing.

## Task Setup and Turn Structure

The task requires an agent to configure a system setting, perform an unrelated operation, and then implicitly validate the configuration. The turn structure is as follows:

**Turn 1 (Conversation stream):** The user provides a configuration request: "Set the API rate limit to 100 requests per minute." This establishes the target configuration value (100) in the conversation stream.

**Turn 2 (Tool stream):** The agent must call `set_rate_limit(limit=100)`, which configures the system and returns:
```json
{
  "status": "configured",
  "current_limit": 100,
  "config_id": "cfg_123"
}
```
This establishes the configuration in the tool output stream and environment state.

**Turn 3 (Distractor, Tool stream):** The agent must call an unrelated tool `get_system_status()`, which returns:
```json
{
  "uptime": 3600,
  "active_connections": 42
}
```
This distractor step creates temporal distance between configuration and validation, preventing solutions that rely on adjacency or immediate context.

**Turn 4 (Implicit validation, Multi-stream):** The agent must call `validate_config(limit=100)`, which requires the rate limit value (100) from Turn 1 and the configuration status from Turn 2. The function returns:
```json
{
  "valid": true,
  "message": "limit matches configured value: 100"
}
```
if validation succeeds, or:
```json
{
  "valid": false,
  "message": "limit mismatch" | "missing required parameter: limit"
}
```
if validation fails. The validation succeeds only if: (a) the rate limit value from Turn 1 matches the configured value from Turn 2, and (b) the environment state (current_limit) matches the configured value. The agent receives no explicit instruction to validate; validation is implicit in the task requirement that the configuration be verified.

## Task-Grounded Dependencies

The following information is necessary prior information for Turn 4, determined independently of model behavior:

1. **Rate limit value (100) from Turn 1 (conversation stream)**: Turn 4's validation requires comparing the configured value against the target value. Without the target value from Turn 1, validation cannot determine correctness. This is a task dependency: the validation function requires both the target and configured values to compute a result.

2. **Configuration status and current_limit from Turn 2 (tool output stream)**: Turn 4 must know that configuration occurred (status: "configured") and what value was actually set (current_limit: 100) to validate correctly. This is a tool dependency: the validation function requires the configuration tool's output to determine what was configured.

3. **Environment state consistency**: Turn 4's validation must check that the environment state (current_limit) matches both the target value from Turn 1 and the configured value from Turn 2. This is a state dependency: validation requires comparing across conversation, tool output, and environment streams.

The distractor in Turn 3 ensures that Turn 4 cannot rely on adjacency: the configuration information is separated from validation by an unrelated operation, requiring retention across non-adjacent turns.

## Outcome-Based Level Distinction

We distinguish retention levels using only outcome-based signals observable from task completion, error patterns, and efficiency signals:

**Level 0 (Information Loss):**
- **Task completion**: Task fails
- **Error pattern**: Turn 4 calls `validate_config()` without the rate limit parameter, producing error "Missing required parameter: limit", OR Turn 4 calls `get_current_limit()` to re-query information already returned in Turn 2
- **Efficiency signal**: Unnecessary re-query observable from API call logs showing `get_current_limit()` called when limit was already returned in Turn 2
- **Outcome**: Validation returns `{"valid": false, "message": "missing required parameter: limit"}` or incorrect validation result due to missing prior information

**Level 1 (Retained but Misapplied):**
- **Task completion**: Task fails
- **Error pattern**: Turn 4 uses rate limit from Turn 1 (conversation stream retained) but ignores configured status from Turn 2 (tool stream not coordinated), OR validates using incorrect comparison logic (e.g., checks if limit > 100 instead of limit == 100)
- **Efficiency signal**: No unnecessary re-queries, but incorrect tool call parameters or validation logic
- **Outcome**: Validation returns `{"valid": false, "message": "limit mismatch"}` when limit is actually correct, or `{"valid": true}` when it's wrong, due to misapplication of retained information

**Level 2 (Coherent Multi-Stream Coordination):**
- **Task completion**: Task succeeds
- **Error pattern**: None
- **Efficiency signal**: No unnecessary re-queries, correct tool call sequence with proper parameters
- **Outcome**: Validation returns `{"valid": true, "message": "limit matches configured value: 100"}` indicating successful coordination across conversation (Turn 1 value), tool output (Turn 2 status), and environment state

## Why This Task Cannot Be Solved by Adjacency, Parameter Passing, or Instruction-Following

The distractor in Turn 3 creates temporal distance between configuration (Turn 2) and validation (Turn 4), preventing adjacency-based solutions. The validation requires information from two non-adjacent turns (rate limit value from Turn 1, configuration status from Turn 2) with no direct parameter passing mechanism between them. Turn 4 contains no explicit instruction to validate; the validation requirement is implicit in the task structure, requiring the agent to determine that validation is necessary based on the configuration action in Turn 2, not from explicit instructions. This task structure ensures that successful completion requires genuine cross-turn information retention across multiple streams, not surface-level pattern matching or instruction compliance.



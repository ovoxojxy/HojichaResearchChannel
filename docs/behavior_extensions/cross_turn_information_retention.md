# Cross-Turn Information Retention: Specification Document

## 1. Definition and Scope

**Cross-turn information retention** is a multi-stream coordination behavior where models maintain and apply information across conversation history, tool outputs, and environment state over multiple turns, observable through semantic consistency and structural patterns.

### Three Information Streams

1. **Conversation history**: Prior turns in the dialogue, including user inputs and model responses
2. **Tool outputs**: Results returned from tool invocations (API calls, database queries, function executions)
3. **Environment state**: External state changes resulting from agent actions (file system changes, database updates, configuration modifications)

### What Counts

- Information maintained across turns without explicit linguistic markers (implicit retention)
- Semantic consistency with prior context even without direct references
- Structural dependencies between tool calls, state transitions, and conversation turns
- Cross-stream integration where information from multiple streams is coordinated

### What Doesn't Count

- Single-turn information use (no cross-turn coordination)
- Explicit references that don't correspond to information actually used in reasoning (false positives)
- Information available immediately in the current turn (redundant marking)
- Stylistic verbosity that doesn't correlate with functional retention

## 2. 0/1/2 Rubric

### Level 0: Information Loss

**Observable markers:**
- **Contradictions with prior context**: Current turn contradicts information from earlier turns or tool outputs (detectable via semantic conflict analysis)
- **Re-querying already obtained information**: Agent queries for data that was returned in prior tool calls or stated in conversation
- **Semantic inconsistency**: Current response is semantically disconnected from prior context (low similarity scores, no dependency on prior information)

**Example**: Agent calls `get_user_preferences(user_id)` in turn 2, receives preferences, then in turn 4 calls `get_user_preferences(user_id)` again instead of using the prior output.

### Level 1: Retained but Misapplied

**Observable markers:**
- **Semantic consistency maintained but wrong application**: Agent's response is semantically coherent with prior context but applies information incorrectly (e.g., uses correct data with wrong logic)
- **Single-stream coordination**: Agent maintains information within one stream (conversation OR tools OR environment) but fails to coordinate across streams (e.g., uses conversation history but ignores relevant tool outputs)
- **Partial retention**: Agent maintains some prior information but loses or misapplies other relevant pieces

**Example**: Agent correctly retrieves user preferences from turn 2 but applies them with incorrect filtering logic in turn 4, or uses conversation context but ignores tool outputs that contradict the conversation.

### Level 2: Coherent Multi-Stream Coordination

**Observable markers:**
- **Semantic consistency across all streams**: Responses are semantically coherent with conversation history, tool outputs, and environment state
- **Cross-stream integration**: Agent uses information from multiple streams (conversation + tools, or tools + environment) in coordinated fashion
- **Correct application**: Information from prior turns or tool outputs is applied correctly to current decisions

**Example**: Agent retrieves preferences (tool output), references prior conversation about constraints (conversation), checks current environment state, and correctly applies all three streams to make a decision.

### Auxiliary Signal (Weak)

**Explicit linguistic references** ("as mentioned before", direct quotes, turn number references) provide supporting evidence but are not required. Models can achieve level 2 through semantic consistency and structural patterns without explicit markers. These references should be discounted when:
- They occur in contexts where referenced information is immediately available in the current turn (redundant marking)
- They appear in models with high baseline verbosity that don't correlate with task success
- They reference information that isn't actually used in the current reasoning (false positives)

## 3. Observable Markers

### Structural Indicators

#### 3.1 Tool Dependency

A tool dependency exists when tool call T_n uses output from tool call T_m (m < n) as a parameter or in its decision logic.

**Observable markers:**
- **Parameter overlap**: T_n's parameters contain values extracted from T_m's output (string matching or structured data extraction)
- **Conditional tool invocation**: T_n is only invoked if T_m's output satisfies a condition
- **Output transformation**: T_n processes or filters T_m's output

**Example**: Agent calls `get_user_preferences(user_id)` in step 2, then calls `filter_products(preferences=prefs_from_step2)` in step 4. Dependency is present if step 4's `preferences` parameter matches step 2's output structure.

#### 3.2 State Incoherence Detection

State incoherence occurs when an agent's actions contradict prior state representations.

**Detectable via:**
- **Value contradictions**: Agent asserts X in turn N, then asserts not-X in turn M without explicit retraction
- **Reference inconsistencies**: Agent uses identifier ID in turn N, then uses different identifier for the same entity in turn M
- **Action-state mismatches**: Agent performs action A that requires state S, but prior actions established not-S

**Example**: Agent sets `status="active"` in step 3, then in step 5 performs `deactivate()` without changing status, or queries using `status="inactive"` without acknowledging the contradiction.

#### 3.3 Cross-Stream Coordination

Measure whether agents integrate information across conversation history, tool outputs, and environment state.

**Signals:**
- **Tool-conversation integration**: Agent uses conversation input to parameterize tool calls, then uses tool output to inform subsequent conversation responses
- **Environment-state awareness**: Agent's actions are consistent with environment state changes from prior tool calls
- **Multi-stream dependencies**: Agent's decision requires information from multiple streams (e.g., conversation context + tool output) but only uses one

**Failure mode**: Agent maintains explicit conversation references ("as you mentioned") but ignores relevant tool outputs or environment changes.

#### 3.4 Memory Pattern Signals

Track information persistence vs. eviction:

- **Re-query patterns**: Agent queries for information already returned by prior tool calls (indicates eviction)
- **Parameter reuse**: Agent reuses values from earlier tool outputs in later tool calls (indicates retention)
- **Context window utilization**: Whether agent preserves critical information as context grows (measure via information-theoretic overlap between early and late context windows)

### Semantic Consistency Markers

**Implicit retention success criterion**: A model demonstrates implicit retention when its current-turn response is semantically consistent with prior-turn information that was necessary for that response, even without explicit linguistic markers.

**Operationalization:**
- **Semantic similarity**: Cosine similarity between current response and prior context (threshold: >0.7)
- **Absence of contradictions**: No semantic conflicts with prior information
- **Coherence requirement**: Decisions that are only coherent given prior context

If a model's turn N response requires information from turn M to be coherent, and the response is coherent, implicit retention is present regardless of explicit markers.

### Explicit Linguistic References

**Discounting rules**: Discount explicit references when:
- They occur in contexts where the referenced information is immediately available in the current turn (redundant marking)
- They appear in models with high baseline verbosity (measured by average tokens per turn) that don't correlate with task success
- They reference information that isn't actually used in the current reasoning (false positives)

Ignore explicit references that don't correspond to information actually required for the current step.

## 4. Controls and Falsification Criteria

### Implicit Retention Success Criterion

A model demonstrates implicit retention when its current-turn response is semantically consistent with prior-turn information that was necessary for that response, even without explicit linguistic markers. Operationalize through: (a) semantic similarity between current response and prior context (threshold: >0.7 cosine similarity), (b) absence of contradictions with prior information, (c) decisions that are only coherent given prior context. If a model's turn N response requires information from turn M to be coherent, and the response is coherent, implicit retention is present regardless of explicit markers.

### Explicit Reference Discounting Rules

Discount explicit references when: (a) they occur in contexts where the referenced information is immediately available in the current turn (redundant marking), (b) they appear in models with high baseline verbosity (measured by average tokens per turn) that don't correlate with task success, (c) they reference information that isn't actually used in the current reasoning (false positives). Ignore explicit references that don't correspond to information actually required for the current step.

### Control Condition 1: Verbosity-Matched Comparison

Compare trajectories with high explicit reference frequency against trajectories with zero explicit references, matched for: total tokens per trajectory, model verbosity baseline, and task complexity. If zero-reference trajectories succeed at equivalent rates, explicit markers are stylistic artifacts of verbose models, not functional retention mechanisms. Measure success rates across matched pairs and test for equivalence (not just correlation).

### Control Condition 2: Instruction-Following Confound

Test whether models trained or prompted to "reference prior context" show increased explicit markers without corresponding increases in task success. If explicit reference frequency increases under instruction-following prompts but success rates don't, markers are byproducts of instruction compliance rather than retention mechanisms. Compare: baseline models vs. models with explicit "reference earlier turns" instructions, controlling for task difficulty.

### Mechanism vs. Byproduct Test

**Explicit markers are the mechanism if:**
- Reference frequency predicts success independently of verbosity and instruction-following
- Removing explicit references (via post-processing) degrades performance
- Implicit retention (measured via semantic consistency) doesn't fully account for success

**They're a byproduct if:**
- Verbosity-matched zero-reference models succeed equivalently
- Instruction-following increases markers without improving success
- Explicit markers correlate with verbosity but not with task success after controlling for verbosity

### Falsification Criteria

The explicit reference → success claim is invalidated if:

1. **Zero-reference equivalence**: Zero-reference trajectories succeed at ≥90% of high-reference success rates on identical tasks
2. **Verbosity correlation**: Explicit reference frequency correlates more strongly with verbosity (r>0.6) than with task success (r<0.3)
3. **Implicit retention priority**: Models with high explicit markers but low implicit retention (semantic inconsistency) fail at higher rates than models with low explicit markers but high implicit retention

## 5. Structural Signals

### How Structural Signals Complement/Override Linguistic Markers

**Structural signals override linguistic markers when:**
- Agent produces explicit references ("as mentioned before") but tool dependencies are missing (linguistic marker is false positive)
- Agent has zero explicit references but strong tool dependencies and state coherence (linguistic marker is false negative)
- Agent shows high explicit reference frequency but state incoherence or missing cross-stream coordination (linguistic markers mask structural failures)

**Structural signals complement linguistic markers when both align**: High explicit reference frequency + strong tool dependencies + state coherence indicates robust multi-stream retention.

### Signals That Survive Verbosity Suppression

All structural signals survive verbosity suppression:
- **Tool dependencies**: Observable from execution traces (parameter matching, conditional invocation patterns)
- **State incoherence**: Observable from action-state contradictions
- **Cross-stream coordination**: Observable from tool-conversation integration patterns
- **Memory patterns**: Observable from re-query behavior and parameter reuse

Linguistic markers fail under verbosity suppression, but structural signals are independent of text output.

## 6. Minimal Toy Task

### Three-Step Tool-Using Task

**Task specification:**
1. Agent calls `get_config(key="api_endpoint")` → returns `"https://api.example.com"`
2. Agent calls `validate_endpoint(url=?)` → should use endpoint from step 1
3. Agent calls `make_request(endpoint=?, data=?)` → should use validated endpoint from step 2

**Linguistic-only diagnostic**: Agent might say "I'll use the endpoint from step 1" (explicit reference) but actually pass wrong URL or re-query instead of using prior output.

**Structural diagnostic**: Check if step 2's `url` parameter matches step 1's output, and if step 3's `endpoint` parameter matches step 2's validated output.

**Failure mode**: Agent produces coherent language ("using the endpoint we validated") but tool dependencies are broken (parameters don't match prior outputs), demonstrating why linguistic-only diagnostics fail.

This task requires cross-turn retention of tool outputs, not just conversation context. Success requires maintaining information from tool outputs across steps, and failure modes include re-querying step 1 data in step 3 instead of using prior tool output, or using incorrect parameters that don't match prior outputs.

## 7. Limitations and Constraints

### No Intent Inference

All markers must be observable from traces without inferring internal states, confidence levels, or intentional behavior. We measure what agents do, not what they "intend" to do.

### Observable Traces Only

All measurements must be derivable from:
- Conversation history (text)
- Tool call sequences and outputs
- Environment state changes
- Structural patterns (parameter dependencies, state transitions)

No access to model internals, attention weights, or hidden states.

### Compatibility with Original Paper's Behavioral Philosophy

This specification extends the original paper's focus on observable behaviors rather than internal cognitive processes. It maintains the principle that behaviors should be:
- Measurable from external traces
- Distinguishable through observable markers
- Classifiable without inferring internal mechanisms
- Applicable across different model architectures and deployment settings

The extension adds multi-stream coordination to capture agentic settings where information flows through multiple channels (conversation, tools, environment), while preserving the original paper's commitment to behavioral observability.



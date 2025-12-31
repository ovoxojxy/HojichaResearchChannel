# Evaluation Logic Stress-Test: Alternative Explanations and Falsification

This document stress-tests the evaluation logic for cross-turn information retention against alternative explanations that reviewers might propose. It demonstrates how existing controls and falsification criteria rule out these alternatives, using equivalence testing and confidence intervals (no fixed thresholds).

## Alternative Explanation 1: Instruction-Following Confound

**Reviewer claim**: Models succeed by following task instructions rather than demonstrating retention. In the deferred configuration validation task, if the task structure implies dependencies (e.g., Turn 4 should validate using information from Turns 1 and 2), success measures instruction compliance, not retention capability.

**How existing controls rule this out**: Control Condition 2 (Instruction-Following Confound) tests whether instruction-following prompts increase markers without improving success. If instruction-following explains success, then: (a) models with explicit "reference earlier turns" instructions should show increased structural retention (tool dependencies, correct parameter usage) without corresponding success improvements, or (b) the interaction effect (instruction × marker frequency on success) should have a 95% confidence interval that excludes zero, indicating instruction-following drives success independently of retention.

The retention claim is falsified if instruction-following prompts increase structural signals (e.g., correct `validate_config(limit=100)` parameter usage) but success rates don't improve, or if the instruction × retention interaction coefficient's confidence interval excludes zero while the retention main effect's confidence interval includes zero.

## Alternative Explanation 2: Task Ease Confound

**Reviewer claim**: The deferred configuration validation task is trivially easy—models succeed through simple parameter passing or variable binding, not retention. Success measures basic tool-calling capability, not cross-turn retention.

**How existing controls rule this out**: The structural diagnostic (outcome-based indicators) distinguishes retention from parameter passing. If task ease explains success, then: (a) models should succeed even when retention dependencies are broken (e.g., Turn 4 calls `validate_config()` without the rate limit parameter, or re-queries `get_current_limit()` instead of using Turn 2's output), or (b) success rates should be equivalent between trajectories with correct retention (Turn 4 uses rate limit from Turn 1 and configuration status from Turn 2) and trajectories with broken retention (Turn 4 re-queries or uses incorrect parameters).

The retention claim is falsified if equivalence testing (TOST) shows that trajectories with broken retention dependencies (Turn 4 missing rate limit parameter, or re-querying Turn 2 information) succeed at rates statistically equivalent to trajectories with correct retention, with the 90% confidence interval for the success rate difference falling entirely within the equivalence margin.

## Alternative Explanation 3: Verbosity Confound

**Reviewer claim**: Models with higher verbosity (more tokens, more explanation) naturally produce more explicit references and succeed more, not because retention matters but because verbosity correlates with general capability.

**How existing controls rule this out**: Control Condition 1 (Verbosity-Matched Comparison) matches trajectories on verbosity and compares success rates. The Mechanism vs. Byproduct Test requires that reference frequency predicts success independently of verbosity (multiple regression with confidence intervals). The retention claim is falsified if: (a) verbosity-matched zero-reference trajectories succeed equivalently to high-reference trajectories (TOST equivalence test), or (b) the 95% confidence interval for the correlation between retention (structural signals, outcome-based indicators) and verbosity excludes zero and is substantially larger than the 95% confidence interval for the correlation between retention and task success (after controlling for verbosity via partial correlation or regression with verbosity as covariate).

## Alternative Explanation 4: General Capability Confound

**Reviewer claim**: Better models (higher general capability) naturally demonstrate better retention, not because retention is a distinct behavior but because capability correlates with all behaviors. The evaluation measures general capability, not retention specifically.

**How existing controls rule this out**: The structural diagnostic isolates retention from general capability by measuring outcome-based indicators (task completion, error patterns, efficiency signals) that are independent of model size or general performance. If general capability explains success, then: (a) retention (correct parameter usage, absence of re-queries, successful validation outcomes) should correlate more strongly with general capability metrics (e.g., model size, baseline task performance) than with task success after controlling for capability, or (b) models with high general capability but broken retention (Turn 4 re-queries or uses incorrect parameters) should succeed equivalently to models with low general capability but correct retention.

The retention claim is falsified if the 95% confidence interval for the correlation between retention and general capability (controlling for task success) excludes zero and is substantially larger than the correlation between retention and task success (controlling for general capability), or if equivalence testing shows that capability-matched trajectories with broken retention succeed equivalently to trajectories with correct retention.

## Results that would falsify the claim

The cross-turn information retention claim is invalidated if any of the following empirical results are observed:

- **Structural dependency equivalence**: Trajectories with broken retention dependencies (Turn 4 calls `validate_config()` without the rate limit parameter, or re-queries `get_current_limit()` instead of using Turn 2's output) succeed at rates statistically equivalent to trajectories with correct retention (TOST equivalence test, 90% confidence interval within equivalence margin). This indicates retention is not necessary for success.

- **Verbosity correlation dominance**: The 95% confidence interval for the correlation between retention (outcome-based indicators) and verbosity excludes zero and is substantially larger (non-overlapping intervals) than the 95% confidence interval for the correlation between retention and task success (after controlling for verbosity). This indicates retention is a byproduct of verbosity, not a functional mechanism.

- **Instruction-following independence**: Instruction-following prompts increase structural retention signals (correct parameter usage) without improving success rates (90% confidence interval for success rate difference includes zero), or the instruction × retention interaction coefficient's confidence interval excludes zero while retention main effect includes zero. This indicates success is driven by instruction compliance, not retention.

- **Capability correlation dominance**: The 95% confidence interval for the correlation between retention and general capability (controlling for success) excludes zero and is substantially larger than retention-success correlation (controlling for capability). This indicates retention is a proxy for general capability, not a distinct behavior.

- **Implicit retention priority**: Models with correct structural dependencies (Turn 4 uses correct parameters from Turns 1 and 2) but low implicit retention (semantic inconsistency with prior context) fail at significantly higher rates than models with broken structural dependencies but high implicit retention (statistical test with confidence intervals). This indicates structural signals don't capture functional retention.



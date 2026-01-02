#!/usr/bin/env python3
"""
Partial Observability Stress Test for pilot_v0.2_paired trajectories (validate_config_v2)

This tests whether structured error codes from validate_config_v2 resolve the ambiguity
identified in the pilot_v0.1 analysis.

Under partial observability, we observe:
- Tool call sequence (names and order)
- Error codes and structured error fields
- Final validation outcome

We CANNOT observe:
- Conversation history (hidden)
- Tool outputs beyond error information (sanitized)
"""

import json
import csv
from pathlib import Path


def extract_partial_observable_signals_v2(trajectory):
    """Extract only what's observable under partial observability with validate_config_v2."""
    tool_sequence = []
    error_info = []
    final_outcome = trajectory.get('final_outcome', 'unknown')
    
    for turn in trajectory['turns']:
        if turn['type'] == 'tool_call':
            tool_sequence.append(turn['tool'])
            result = turn.get('result', {})
            
            # With validate_config_v2, we can now observe structured error codes
            if 'error_code' in result:
                error_info.append({
                    'error_code': result['error_code'],
                    'observed_limit': result.get('observed_limit'),
                    'expected_limit': result.get('expected_limit'),
                    'message': result.get('message', '')
                })
            elif result.get('valid') is False and 'message' in result:
                # Legacy format (shouldn't occur in v2 traces but handling for completeness)
                error_info.append({
                    'error_code': 'LEGACY',
                    'message': result['message']
                })
    
    return {
        'tool_sequence': tool_sequence,
        'error_info': error_info,
        'final_outcome': final_outcome
    }


def classify_under_partial_observability_v2(traj_id, signals):
    """
    Classify trajectory based on partial observable signals with validate_config_v2.
    
    The structured error codes should resolve the ambiguity from pilot_v0.1:
    - MISMATCH with observed != expected → Level 1 (wrong value passed)
    - VALIDATION_FAILURE with observed == expected → system failure (agent did Level 2)
    - MISSING_PARAMETER → Level 0 (information loss)
    
    Returns: (label, explanation)
    """
    seq = signals['tool_sequence']
    errors = signals['error_info']
    outcome = signals['final_outcome']
    
    # Level 0 indicators (information loss) - CLEAR
    
    # Missing parameter errors
    if any(e.get('error_code') == 'MISSING_PARAMETER' for e in errors):
        return ("0", "MISSING_PARAMETER error code indicates information loss from prior turns")
    
    # Re-query patterns (observable from tool sequence)
    if 'get_current_limit' in seq or 'check_rate_limit' in seq:
        return ("0", "Re-query pattern: querying information already available from prior tool output")
    
    # Incomplete execution
    if 'validate_config_v2' not in seq and 'validate_config' not in seq:
        return ("0", "Incomplete: never called validation")
    
    # Level 1 indicators (information retained but misapplied) - NOW CLEAR with structured errors
    
    # MISMATCH with observed != expected
    for e in errors:
        if e.get('error_code') == 'MISMATCH':
            obs = e.get('observed_limit')
            exp = e.get('expected_limit')
            if obs is not None and exp is not None and obs != exp:
                return ("1", f"MISMATCH: observed_limit={obs}, expected_limit={exp} - agent passed wrong value but retained some information")
    
    # System failure (agent did Level 2 coordination, system failed) - NOW DISTINGUISHABLE
    
    # VALIDATION_FAILURE with observed == expected
    for e in errors:
        if e.get('error_code') == 'VALIDATION_FAILURE':
            obs = e.get('observed_limit')
            exp = e.get('expected_limit')
            if obs is not None and exp is not None and obs == exp:
                return ("system_failure", f"VALIDATION_FAILURE: observed={obs}, expected={exp} - agent passed correct value, system failed")
    
    # Level 2 indicators (clean success) - CLEAR
    if outcome == 'success' and len(errors) == 0:
        return ("2", "Clean success with correct tool sequence and no errors")
    
    # Legacy/unknown errors (shouldn't happen with v2)
    if any(e.get('error_code') == 'LEGACY' for e in errors):
        return ("ambiguous", "Legacy error format without structured fields")
    
    # Any other success
    if outcome == 'success':
        return ("2", "Task success with no observable errors")
    
    # Any other failure
    if outcome == 'failure':
        return ("ambiguous", "Failure without clear error code classification")
    
    return ("ambiguous", "Insufficient observable signals to classify")


def main():
    # Read traces
    traces_file = Path(__file__).parent.parent / 'data' / 'traces' / 'pilot_v0.2_paired.jsonl'
    output_file = Path(__file__).parent.parent / 'data' / 'labels' / 'pilot_v0.2_paired_labels_ra3_partial.csv'
    
    results = []
    
    with open(traces_file, 'r') as f:
        for line in f:
            if line.strip():
                trajectory = json.loads(line)
                traj_id = trajectory['trajectory_id']
                
                # Extract partial observable signals
                signals = extract_partial_observable_signals_v2(trajectory)
                
                # Classify
                label, explanation = classify_under_partial_observability_v2(traj_id, signals)
                
                results.append({
                    'trace_id': traj_id,
                    'label_or_ambiguous': label,
                    'explanation': explanation
                })
    
    # Write results
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['trace_id', 'label_or_ambiguous', 'explanation'])
        writer.writeheader()
        writer.writerows(results)
    
    # Summary
    label_counts = {}
    for r in results:
        label = r['label_or_ambiguous']
        label_counts[label] = label_counts.get(label, 0) + 1
    
    print(f"Processed {len(results)} trajectories")
    print(f"Label distribution: {label_counts}")
    print(f"Results written to: {output_file}")
    
    # Calculate ambiguity rate
    ambiguous_count = label_counts.get('ambiguous', 0)
    total_count = len(results)
    ambiguity_rate = (ambiguous_count / total_count * 100) if total_count > 0 else 0
    print(f"\nAmbiguity rate: {ambiguity_rate:.1f}% ({ambiguous_count}/{total_count})")


if __name__ == '__main__':
    main()


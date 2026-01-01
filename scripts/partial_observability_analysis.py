#!/usr/bin/env python3
"""
Partial Observability Stress Test for pilot_v0.1 trajectories

Under partial observability, we only observe:
- Tool call sequence (names and order)
- Error messages
- Final validation outcome

We CANNOT observe:
- Conversation history (hidden)
- Tool outputs (sanitized)
- Parameter values

Task: Assign Level 0/1/2 or mark as "ambiguous" based solely on these limited signals.
"""

import json
import csv
from pathlib import Path


def extract_partial_observable_signals(trajectory):
    """Extract only what's observable under partial observability."""
    tool_sequence = []
    error_messages = []
    final_outcome = trajectory.get('final_outcome', 'unknown')
    
    for turn in trajectory['turns']:
        if turn['type'] == 'tool_call':
            tool_sequence.append(turn['tool'])
            result = turn.get('result', {})
            
            # Only error messages are observable, not full outputs
            if 'message' in result and result.get('valid') is False:
                error_messages.append(result['message'])
            elif 'message' in result and 'error' in result.get('status', '').lower():
                error_messages.append(result['message'])
    
    return {
        'tool_sequence': tool_sequence,
        'error_messages': error_messages,
        'final_outcome': final_outcome
    }


def classify_under_partial_observability(traj_id, signals):
    """
    Classify trajectory based only on partial observable signals.
    
    Returns: (label, explanation)
    where label is "0", "1", "2", or "ambiguous"
    """
    seq = signals['tool_sequence']
    errors = signals['error_messages']
    outcome = signals['final_outcome']
    
    # Level 0 indicators (information loss) - CLEAR under partial observability
    
    # Missing parameter errors
    if any('Missing required parameter' in e for e in errors):
        return ("0", "Missing parameter error indicates information loss from prior turns")
    
    # No configuration found (set_rate_limit failed)
    if any('No configuration found' in e for e in errors):
        return ("0", "Configuration never established; set_rate_limit failed")
    
    # Re-query patterns (observable from tool sequence)
    if 'get_current_limit' in seq or 'check_rate_limit' in seq:
        # These tools query info already returned by set_rate_limit
        return ("0", "Re-query pattern: querying information already available from prior tool output")
    
    # Incomplete execution (never called validate_config)
    if 'validate_config' not in seq:
        return ("0", "Incomplete: never called validate_config")
    
    # Level 2 indicators (clean success) - CLEAR under partial observability
    if outcome in ['success'] and len(errors) == 0:
        # Clean success with correct sequence
        if seq == ['set_rate_limit', 'get_system_status', 'validate_config']:
            return ("2", "Clean success with correct tool sequence and no errors")
    
    # Ambiguous cases - cannot distinguish Level 0 vs Level 1
    if 'limit mismatch' in ' '.join(errors):
        # "limit mismatch" could mean:
        # - Level 0: wrong parameter was retained (e.g., used wrong value from conversation)
        # - Level 1: correct parameter retained but wrong value/logic applied
        # Without seeing params, we cannot distinguish
        return ("ambiguous", "limit mismatch error - cannot distinguish information loss (L0) vs misapplication (L1) without parameter visibility")
    
    # Success with wrong value (outcome indicates wrong value but task succeeded)
    if 'wrong_value' in outcome:
        # Can't detect conversation stream failure without seeing params
        return ("ambiguous", "Success but potentially wrong value - cannot verify conversation stream coordination without parameter visibility")
    
    # Any other success (may have extra params we can't verify)
    if outcome == 'success' and len(errors) == 0:
        return ("2", "Task success with no observable errors")
    
    # Failure without clear Level 0 markers
    if outcome == 'failure':
        return ("ambiguous", "Failure without clear Level 0 markers - cannot determine if information loss or misapplication")
    
    return ("ambiguous", "Insufficient observable signals to classify")


def main():
    # Read traces
    traces_file = Path(__file__).parent.parent / 'data' / 'traces' / 'pilot_v0.1.jsonl'
    output_file = Path(__file__).parent.parent / 'data' / 'labels' / 'pilot_v0.1_labels_ra3_partial.csv'
    
    results = []
    
    with open(traces_file, 'r') as f:
        for line in f:
            if line.strip():
                trajectory = json.loads(line)
                traj_id = trajectory['trajectory_id']
                
                # Extract partial observable signals
                signals = extract_partial_observable_signals(trajectory)
                
                # Classify
                label, explanation = classify_under_partial_observability(traj_id, signals)
                
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


if __name__ == '__main__':
    main()


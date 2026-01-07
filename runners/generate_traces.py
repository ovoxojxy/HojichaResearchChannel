import json
from agents.naive_agent import NaiveAgent
from agents.retention_agent import RetentionAgent
from runners.run_episode import run_episode


def generate_paired_traces(output_file="data/traces/pilot_v0.3.jsonl", num_trajectories=50):
    """
    Generate paired trajectories with v1 and v2 validators.
    Each trajectory is run twice with the same agent behavior,
    only the validator output schema differs.
    """
    # Use existing agents - they provide diverse failure modes
    agents = [
        NaiveAgent(),  # Level 0: missing params
        RetentionAgent(),  # Level 2: clean success
    ]
    
    # Repeat agents to reach num_trajectories
    agent_list = []
    for i in range(num_trajectories):
        agent_list.append(agents[i % len(agents)])
    
    with open(output_file, "w") as f:
        for traj_idx, agent in enumerate(agent_list, 1):
            # Run with v1 validator
            trace_v1 = run_episode(agent, validator_version="v1")
            
            # Run with v2 validator (same agent, same behavior)
            trace_v2 = run_episode(agent, validator_version="v2")
            
            # Sanity check: tool sequences should be identical
            tools_v1 = [turn.get("tool") for turn in trace_v1 if "tool" in turn]
            tools_v2 = [turn.get("tool") for turn in trace_v2 if "tool" in turn]
            
            if tools_v1 != tools_v2:
                print(f"WARNING: Tool sequences differ for trajectory {traj_idx}")
                print(f"  v1: {tools_v1}")
                print(f"  v2: {tools_v2}")
            
            # Extract params for validation step (should be identical)
            params_v1 = None
            params_v2 = None
            for turn in trace_v1:
                if turn.get("tool") in ["validate_config", "validate_config_v2"]:
                    params_v1 = turn.get("params")
                    break
            for turn in trace_v2:
                if turn.get("tool") in ["validate_config", "validate_config_v2"]:
                    params_v2 = turn.get("params")
                    break
            
            if params_v1 != params_v2:
                print(f"WARNING: Validation params differ for trajectory {traj_idx}")
                print(f"  v1: {params_v1}")
                print(f"  v2: {params_v2}")
            
            # Create trajectory records with metadata
            traj_id_base = f"traj_v3_{traj_idx:03d}"
            
            # Determine final outcome
            def get_outcome(trace):
                for turn in trace:
                    if "result" in turn:
                        result = turn["result"]
                        if result.get("valid") is True:
                            return "success"
                    if "error" in turn:
                        return "failure"
                return "failure"
            
            # V1 trajectory
            trajectory_v1 = {
                "trajectory_id": f"{traj_id_base}_v1",
                "turns": trace_v1,
                "final_outcome": get_outcome(trace_v1),
                "metadata": {
                    "validator_version": "v1",
                    "agent": agent.name,
                    "base_trajectory_id": traj_id_base
                }
            }
            
            # V2 trajectory
            trajectory_v2 = {
                "trajectory_id": f"{traj_id_base}_v2",
                "turns": trace_v2,
                "final_outcome": get_outcome(trace_v2),
                "metadata": {
                    "validator_version": "v2",
                    "agent": agent.name,
                    "base_trajectory_id": traj_id_base
                }
            }
            
            # Write both trajectories
            f.write(json.dumps(trajectory_v1) + "\n")
            f.write(json.dumps(trajectory_v2) + "\n")
    
    print(f"Generated {num_trajectories} paired trajectories ({num_trajectories * 2} total entries)")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    generate_paired_traces()
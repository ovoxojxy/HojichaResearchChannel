import json
from tasks.deferred_config_validation.env import TOOLS, ToolError, env


def reset_environment():
    """Reset the environment state between episodes."""
    env.current_limit = None
    env.configured = False
    env.force_validation_failure = False


def run_episode(agent, validator_version="v1"):
    """
    Run an episode with the given agent.
    
    Args:
        agent: The agent to run
        validator_version: "v1" or "v2" - determines which validator to use
                          when agent calls validate_config or validate_config_v2
    
    Returns:
        List of trace entries
    """
    reset_environment()
    trace = []
    memory = {}
    
    # Map validator version to actual tool name
    validator_map = {
        "v1": "validate_config",
        "v2": "validate_config_v2"
    }
    target_validator = validator_map.get(validator_version, "validate_config")

    # Turn 1: Conversation (not a tool call)
    trace.append({
        "turn": 1,
        "type": "conversation",
        "content": "Set the API rate limit to 100 requests per minute."
    })

    # Turns 2-4: Tool calls
    for turn in [2, 3, 4]:
        try:
            action = agent.act(turn, None, memory)
            if action is None:
                continue

            tool_name, params = action
            
            # Normalize validation calls to use the specified validator version
            if tool_name in ["validate_config", "validate_config_v2"]:
                tool_name = target_validator
            
            result = TOOLS[tool_name](**params)

            trace.append({
                "turn": turn,
                "type": "tool_call",
                "tool": tool_name,
                "params": params,
                "result": result
            })

        except ToolError as e:
            trace.append({
                "turn": turn,
                "type": "tool_call",
                "tool": tool_name,
                "params": params,
                "error": e.message
            })
            break

    return trace
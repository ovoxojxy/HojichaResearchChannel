import json
from tasks.deferred_config_validation.env import TOOLS, ToolError


def run_episode(agent):
    trace = []
    memory = {}

    for turn in [1, 2, 3, 4]:
        try:
            action = agent.act(turn, None, memory)
            if action is None:
                continue

            tool_name, params = action
            result = TOOLS[tool_name](**params)

            trace.append({
                "turn": turn,
                "tool": tool_name,
                "params": params,
                "result": result
            })

        except ToolError as e:
            trace.append({
                "turn": turn,
                "tool": tool_name,
                "params": params,
                "error": e.message
            })
            break

    return trace
def classify_outcome(trace):
    tools = [step["tool"] for step in trace]

    # Re-query signal
    if tools.count("get_current_limit") > 0:
        return "Level 0"

    # Error signal
    for step in trace:
        if "error" in step:
            if "Missing required parameter" in step["error"]:
                return "Level 0"
            return "Level 1"

    # Final success
    last = trace[-1]
    if last.get("result", {}).get("valid") is True:
        return "Level 2"

    return "Level 1"
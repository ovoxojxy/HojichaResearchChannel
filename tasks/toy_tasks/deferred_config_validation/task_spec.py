TASK_NAME = "deferred_config_validation"

# Task-grounded necessary prior information
REQUIRED_DEPENDENCIES = {
    "turn_4": {
        "conversation": ["rate_limit_value"],
        "tool_outputs": ["configured", "current_limit"],
        "environment": ["current_limit"]
    }
}

SUCCESS_CONDITION = {
    "valid": True,
    "message": "limit matches configured value"
}
from .tools import (
    set_rate_limit,
    get_system_status,
    get_current_limit,
    validate_config,
    validate_config_v2,
    ToolError,
    env
)

TOOLS = {
    "set_rate_limit": set_rate_limit,
    "get_system_status": get_system_status,
    "get_current_limit": get_current_limit,
    "validate_config": validate_config,
    "validate_config_v2": validate_config_v2
}
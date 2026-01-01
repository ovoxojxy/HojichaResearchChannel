from .tools import (
    set_rate_limit,
    get_system_status,
    get_current_limit,
    validate_config,
    ToolError
)

TOOLS = {
    "set_rate_limit": set_rate_limit,
    "get_system_status": get_system_status,
    "get_current_limit": get_current_limit,
    "validate_config": validate_config
}
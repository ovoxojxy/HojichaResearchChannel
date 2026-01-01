class ToolError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ConfigEnvironment:
    def __init__(self):
        self.current_limit = None
        self.configured = False


env = ConfigEnvironment()


def set_rate_limit(limit: int):
    env.current_limit = limit
    env.configured = True
    return {
        "status": "configured",
        "current_limit": limit,
        "config_id": "cfg_123"
    }


def get_system_status():
    return {
        "uptime": 3600,
        "active_connections": 42
    }


def get_current_limit():
    return {
        "current_limit": env.current_limit
    }


def validate_config(limit: int | None = None):
    if limit is None:
        raise ToolError("Missing required parameter: limit")

    if not env.configured:
        return {"valid": False, "message": "not configured"}

    if limit != env.current_limit:
        return {"valid": False, "message": "limit mismatch"}

    return {"valid": True, "message": "limit matches configured value"}
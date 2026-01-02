class ToolError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ConfigEnvironment:
    def __init__(self):
        self.current_limit = None
        self.configured = False
        self.force_validation_failure = False


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


def validate_config_v2(limit: int | None = None, **kwargs):
    """
    Enhanced validation with structured error codes for disambiguation.
    
    Returns structured error information:
    - MISSING_PARAMETER: limit parameter not provided
    - MISMATCH: observed_limit != expected_limit (agent passed wrong value)
    - VALIDATION_FAILURE: observed_limit == expected_limit but validation failed (system failure)
    """
    # Missing parameter case
    if limit is None:
        return {
            "valid": False,
            "error_code": "MISSING_PARAMETER",
            "message": "Missing required parameter: limit",
            "provided_params": {k: v for k, v in kwargs.items()}
        }
    
    # Configuration not set case
    if not env.configured:
        return {
            "valid": False,
            "error_code": "NO_CONFIGURATION",
            "message": "No configuration found"
        }
    
    # Mismatch case - now shows exactly what was passed vs expected
    if limit != env.current_limit:
        return {
            "valid": False,
            "error_code": "MISMATCH",
            "observed_limit": limit,
            "expected_limit": env.current_limit,
            "message": f"limit mismatch: got {limit}, expected {env.current_limit}"
        }
    
    # Validation failure case - agent passed correct value but system fails
    # This simulates system-side failures (faulty validation logic, edge cases, etc.)
    if env.force_validation_failure:
        return {
            "valid": False,
            "error_code": "VALIDATION_FAILURE",
            "observed_limit": limit,
            "expected_limit": env.current_limit,
            "message": "Validation logic failed despite correct parameters"
        }
    
    # Success case
    return {
        "valid": True,
        "message": "limit matches configured value"
    }
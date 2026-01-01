from .base_agent import BaseAgent

class RetentionAgent(BaseAgent):
    name = "retention"

    def act(self, turn, observation, memory):
        if turn == 1:
            memory["limit"] = 100
            return ("set_rate_limit", {"limit": 100})
        if turn == 2:
            return ("get_system_status", {})
        if turn == 3:
            return ("validate_config", {"limit": memory["limit"]})
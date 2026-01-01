from .base_agent import BaseAgent

class NaiveAgent(BaseAgent):
    name = "naive"

    def act(self, turn, observation, memory):
        if turn == 1:
            return ("set_rate_limit", {"limit": 100})
        if turn == 2:
            return ("get_system_status", {})
        if turn == 3:
            return ("validate_config", {})  # missing limit
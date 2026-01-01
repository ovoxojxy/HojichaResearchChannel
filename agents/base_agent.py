class BaseAgent:
    name = "base"

    def act(self, turn, observation, memory):
        raise NotImplementedError
import json
from agents.naive_agent import NaiveAgent
from agents.requery_agent import RequeryAgent
from agents.retention_agent import RetentionAgent
from runners.run_episode import run_episode

agents = [NaiveAgent(), RequeryAgent(), RetentionAgent()]

with open("data/traces/pilot.jsonl", "w") as f:
    for agent in agents:
        trace = run_episode(agent)
        f.write(json.dumps({
            "agent": agent.name,
            "trace": trace
        }) + "\n")
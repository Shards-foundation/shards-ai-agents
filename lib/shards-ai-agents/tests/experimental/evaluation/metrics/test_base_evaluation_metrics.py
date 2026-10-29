from unittest.mock import MagicMock

import pytest
from shards_ai_agents.agent import Agent
from shards_ai_agents.task import Task


class BaseEvaluationMetricsTest:
    @pytest.fixture
    def mock_agent(self):
        agent = MagicMock(spec=Agent)
        agent.id = "test_agent_id"
        agent.role = "Test Agent"
        agent.goal = "Test goal"
        agent.tools = []
        return agent

    @pytest.fixture
    def mock_task(self):
        task = MagicMock(spec=Task)
        task.description = "Test task description"
        task.expected_output = "Test expected output"
        return task

    @pytest.fixture
    def execution_trace(self):
        return {
            "thinking": ["I need to analyze this data carefully"],
            "actions": ["Gathered information", "Analyzed data"],
        }

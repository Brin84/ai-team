from app.agents.base import BaseAgent

from app.core.agent_types import AGENT_TYPES


class DynamicAgent(BaseAgent):

    def __init__(
        self,
        name: str,
        role: str,
        agent_type: str
    ):

        restrictions = AGENT_TYPES.get(
            agent_type,
            ""
        )

        final_role = f"""
{role}

Дополнительные правила:

{restrictions}
"""

        super().__init__(
            role=final_role
        )

        self.name = name
        self.agent_type = agent_type
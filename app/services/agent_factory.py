from app.services.dynamic_agent import (
    DynamicAgent
)

from app.core.agent_types import (
    AGENT_TYPES
)


class AgentFactory:

    @staticmethod
    def create_agent(
        name: str,
        agent_type: str
    ):

        role = AGENT_TYPES.get(
            agent_type,
            ""
        )

        return DynamicAgent(
            name=name,
            role=role,
            agent_type=agent_type
        )
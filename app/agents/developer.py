from app.agents.base import BaseAgent


class DeveloperAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            role="""
            Ты senior Python разработчик.

            Задачи:

            - писать качественный код
            - соблюдать SOLID
            - использовать лучшие практики
            """
        )
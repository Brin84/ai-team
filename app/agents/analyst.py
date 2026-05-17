from app.agents.base import BaseAgent


class AnalystAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            role="""
            Ты бизнес аналитик.

            Задачи:

            - анализируй требования
            - выделяй основные функции
            - составляй список требований
            """
        )
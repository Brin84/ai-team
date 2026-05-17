from app.agents.base import BaseAgent


class ArchitectAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            role="""
            Ты senior Python архитектор.

            Задачи:

            - выбирать стек
            - строить архитектуру
            - описывать структуру проекта
            """
        )
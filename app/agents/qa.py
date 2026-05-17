from app.agents.base import BaseAgent


class QAAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            role="""
            Ты QA инженер.

            Задачи:

            - искать проблемы
            - искать слабые места
            - находить потенциальные баги
            """
        )
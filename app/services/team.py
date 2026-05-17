class AITeam:

    def __init__(
            self,
            architect,
            developer,
            qa
    ):
        self.architect = architect
        self.developer = developer
        self.qa = qa

    @staticmethod
    def compress(
            text: str,
            limit: int = 500
    ) -> str:
        if not text:
            return ""

        return text[:limit]

    def run(
            self,
            task: str
    ):
        state = {
            "task": task,
            "architecture": "",
            "code": "",
            "review": ""
        }

        # Архитектор

        architecture = self.architect.run(
            f"""
Задача:

{task}

Создай:

1. Стек
2. Структуру проекта
3. Компоненты

Максимум 300 слов.
"""
        )

        state["architecture"] = self.compress(
            architecture,
            500
        )

        # Разработчик

        state["code"] = self.developer.run(
            f"""
        Задача:

        {task}

        Архитектура:

        {state["architecture"]}

        Создай только 3 файла:

        1. app/main.py
        2. app/config.py
        3. requirements.txt

        Верни JSON такого вида:

        {{
            "files": [
                {{
                    "path": "app/main.py",
                    "content": "код"
                }}
            ]
        }}

        Правила:

        - не используй markdown
        - content всегда строка
        - каждый объект содержит path и content
        - ответ начинается с {{
        - ответ заканчивается }}

        Создай файлы проекта.
        """
        )

        # QA

        review = self.qa.run(
            f"""
Проверь проект.

Задача:

{task}

Архитектура:

{state["architecture"]}

Найди:

1. Баги
2. Риски
3. Ошибки

Максимум 200 слов.
"""
        )

        state["review"] = self.compress(
            review,
            300
        )

        return state

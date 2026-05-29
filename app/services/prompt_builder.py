class PromptBuilder:

    @staticmethod
    def planner_prompt(
        task: str
    ) -> str:

        return f"""
Задача:

{task}

Разбей задачу на этапы.

Для каждого этапа укажи:

1. Этап
2. Исполнитель
3. Цель

Кратко.
"""

    @staticmethod
    def architect_prompt(
        task: str,
        plan: str,
        team_errors,
        success_patterns,
        knowledge
    ) -> str:

        return f"""
Задача:

{task}

План:

{plan}

Известные ошибки:

{team_errors}

Успешные решения:

{success_patterns}

Знания команды:

{knowledge}

Спроектируй решение.
"""

    @staticmethod
    def developer_prompt(
        task: str,
        architecture: str,
        team_errors,
        success_patterns,
        knowledge
    ) -> str:

        return f"""
Задача:

{task}

Архитектура:

{architecture}

Известные ошибки:

{team_errors}

Успешные решения:

{success_patterns}

Знания команды:

{knowledge}

Правила:

- Верни только JSON
- Не используй markdown
- Все content должны быть строками
- Все зависимости должны быть в requirements.txt
- Используй os.getenv() для секретов
- Не используй фиктивные токены

Формат:

{{
    "files":[
        {{
            "path":"app/main.py",
            "content":"..."
        }},
        {{
            "path":"requirements.txt",
            "content":"..."
        }}
    ]
}}

Верни только JSON.
"""

    @staticmethod
    def fix_prompt(
        error: str,
        previous_code: str,
        knowledge
    ) -> str:

        return f"""
Исправь проект.

Ошибка:

{error}

Предыдущий ответ:

{previous_code}

Знания команды:

{knowledge}

Верни только JSON.
"""
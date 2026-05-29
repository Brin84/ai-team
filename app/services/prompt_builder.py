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

Правила команды (обязательно соблюдать):

{knowledge}

ЖЁСТКИЕ ОГРАНИЧЕНИЯ:

- Проект должен состоять РОВНО из 2 файлов
- Разрешены только:
  - app/main.py
  - requirements.txt
- Любой другой файл запрещён
- Не создавай database.py
- Не создавай db.py
- Не создавай parser.py
- Не создавай parsers.py
- Не создавай models.py
- Не создавай routers.py
- Не создавай config.py
- Не создавай services.py
- Не используй импорты database
- Не используй импорты db
- Не используй импорты parser
- Не используй импорты parsers
- Не используй импорты models
- Не используй импорты routers
- Не используй импорты config
- Не используй импорты services
- Весь код должен находиться внутри app/main.py
- Все зависимости должны существовать в requirements.txt
- Используй только существующие пакеты PyPI
- Используй os.getenv() для секретов
- Верни только JSON
- Не используй markdown

Формат ответа:

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
    Исправь ТОЛЬКО указанную ошибку.

    Ошибка:

    {error}

    Текущий JSON проекта:

    {previous_code}

    Правила команды:

    {knowledge}

    Обязательные требования:

    - НЕ создавай новый проект
    - НЕ придумывай новую архитектуру
    - Исправь только указанную ошибку
    - Сохрани существующую структуру ответа
    - Должно остаться ровно 2 файла
    - app/main.py
    - requirements.txt
    - Не добавляй новые файлы
    - Не удаляй существующие файлы
    - Все зависимости должны быть в requirements.txt
    - Верни ответ строго в формате JSON
    - Не используй markdown
    - Не добавляй пояснения
    - Не добавляй текст до JSON
    - Не добавляй текст после JSON

    Ожидаемый формат:

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

    Верни только исправленный JSON.
    """
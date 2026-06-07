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

Спроектируй production-ready архитектуру проекта.

Правила:

- Используй многофайловую архитектуру
  если проект содержит
  более одной ответственности

- Разделяй:

  - бизнес-логику
  - модели данных
  - API
  - инфраструктуру
  - конфигурацию

- Продумай масштабируемую
  структуру проекта

- Используй реальные Python-пакеты

- Не добавляй лишние зависимости

- Запрещено добавлять
  stdlib модули
  в requirements

Примеры stdlib:

- sqlite3
- os
- sys
- json
- pathlib
- asyncio

- Используй минимально
  необходимый стек

- Используй минимально
  необходимый стек

- Для MVP архитектуры
  используй минимальное
  количество файлов

- Не создавай файлы
  без необходимости

- Предпочитай компактную
  структуру проекта

- Не создавай сложную
  декомпозицию для MVP

- Максимум 15 файлов

- Используй только современные
  версии библиотек

- Для Telegram используй:
  python-telegram-bot >= 20

- Не используй legacy API:

  - Updater
  - Dispatcher
  - Filters
  - use_context

- Не пиши код

- Не пиши пояснения

- Верни только JSON

Если проект содержит:

- хранение данных →
  app/models/
  app/db/

- бизнес-логику →
  app/services/

- HTTP API →
  app/api/

- утилиты →
  app/utils/

- парсинг →
  parsers

- конфигурацию →
  config.py
- models ОБЯЗАНЫ находиться
  только внутри app/models/

- services ОБЯЗАНЫ находиться
  только внутри app/services/

- database layer ОБЯЗАН находиться
  только внутри app/db/

- utils ОБЯЗАНЫ находиться
  только внутри app/utils/

Запрещено размещать файлы:

- app/user_model.py
- app/booking_service.py
- app/google_sheets_db.py
- app/notification_utils.py

в корне app/
Обязательные файлы:

- app/main.py
- requirements.txt
- requirements.txt
  должен находиться
  ТОЛЬКО в корне проекта

СТРОГО ЗАПРЕЩЕНО создавать:

  - app/requirements.txt
  - src/requirements.txt
Правила project_structure:
Пример ПРАВИЛЬНОЙ структуры:

- app/services/booking_service.py
- app/models/user_model.py
- app/db/google_sheets_db.py
- app/api/telegram_api.py
- app/utils/notification_utils.py

Пример НЕПРАВИЛЬНОЙ структуры:

- app/booking_service.py
- app/user_model.py
- app/google_sheets_db.py
- app/telegram_api.py
- app/notification_utils.py
- Если используются пакеты Python
  с вложенными директориями,
  ОБЯЗАТЕЛЬНО добавляй:

  - __init__.py

- Каждый Python package
  должен содержать __init__.py
- Если используется:

  - app/services/
  - app/models/
  - app/db/
  - app/api/
  - app/utils/

  architect ОБЯЗАН добавить:

  - __init__.py

  внутрь каждой директории
- Названия файлов
  должны отражать
  их ответственность

Плохо:

- api.py
- core.py
- utils.py
- services.py
- models.py

Хорошо:

- booking_service.py
- google_sheets_db.py
- notification_utils.py
- telegram_api.py
- registration_service.py
- user_model.py
- booking_model.py

- Запрещено создавать:

  - services.py
  - utils.py
  - handlers.py
  - models.py
  - api.py
  - core.py

- Каждый файл должен отражать
  ОДНУ ответственность
- В project_structure
  указывай только файлы

- Не добавляй директории
  отдельными элементами

Формат ответа:

{{
    "stack": [],
    "components": [],
    "project_structure": [],
    "requirements": []
}}

Верни только JSON.
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
    
    - Нельзя изменять тип проекта

    Пример:
    
    Если architecture описывает:
    - telegram bot
    
    ЗАПРЕЩЕНО:
    - генерировать FastAPI backend
    - генерировать Django проект
    - генерировать Flask API
    
    - Код ОБЯЗАН соответствовать
      architecture
      
    Известные ошибки:

    {team_errors}

    Успешные решения:

    {success_patterns}

    Правила команды:

    {knowledge}

    Требования:

    - Делай код кратким

    - Не пиши длинные реализации

    - Используй минимальный рабочий код

    - Не добавляй комментарии

    - Каждый file.content должен быть коротким

    - Максимум 80 строк на файл

    - Если проект большой,
      создавай минимальные заглушки

    - Если JSON начинает становиться
      слишком большим,
      упрощай реализации,
      но НЕ пропускай файлы

    - Главное:
      вернуть ПОЛНЫЙ валидный JSON
    - Запрещено удалять файлы,
      уже существующие в проекте
    
    - При исправлении проекта
      изменяй ТОЛЬКО проблемные файлы
    
    - Не переписывай весь проект,
      если ошибка находится
      в одном файле
    
    - Не удаляй requirements.txt
    
    - Не удаляй app/main.py
    
    - Если файл уже существует,
      сохраняй его архитектуру
    - Создавай количество файлов,
      необходимое для реализации
      всей project_structure

    - Минимум 2 файла

    - Максимум 15 файлов

    - Строго следуй
      project_structure
      из архитектуры

    - Пути файлов должны
      совпадать СИМВОЛ В СИМВОЛ
      с project_structure

    - Запрещено изменять:

      - названия файлов
      - регистр символов
      - окончания
      - prefixes
      - suffixes

    ПРИМЕР:

    Если architect указал:

    - app/db/google_sheets_db.py

    ТОЛЬКО этот path допустим.

    Запрещено:

    - app/db/google_sheet_db.py
    - app/google_sheets_db.py
    - google_sheets_db.py

    - Создавай ВСЕ файлы,
      указанные architect

    - Если architect указал файл
      в project_structure,
      ты ОБЯЗАН создать этот файл

    - Запрещено игнорировать
      project_structure

    - Создай все обязательные файлы
      из project_structure

    - Директории создавать
      отдельными объектами НЕ НУЖНО

    - Если project_structure содержит
      файлы внутри:

      - app/services/
      - app/models/
      - app/db/
      - app/api/
      - app/utils/

      обязательно создай
      эти файлы

    - Если создаётся директория:

      - app/services/
      - app/models/
      - app/db/
      - app/api/
      - app/utils/

      ОБЯЗАТЕЛЬНО создавай
      __init__.py внутри директории

    - Каждый импорт должен ссылаться:

      - либо на существующий
        файл проекта

      - либо на dependency
        из requirements.txt

    - Используй абсолютные импорты

    Правильно:

    - from app.config import ...
    - from app.services.booking_service import ...
    - from app.models.user_model import ...

    Неправильно:

    - from config import ...
    - from booking_service import ...
    - from user_model import ...

    - Запрещено импортировать модули,
      для которых не существует файла
    
    - Перед созданием import
      ОБЯЗАТЕЛЬНО проверь,
      существует ли файл
      в project_structure
    
    - Используй imports
      ТОЛЬКО из project_structure
    
    - Запрещено создавать imports
      для файлов,
      отсутствующих
      в project_structure
    
    Пример:
    
    Если отсутствует:
    
    - app/core.py
    
    ЗАПРЕЩЕНО:
    
    - from app.core import ...
    
    Если отсутствует:
    
    - app/database.py
    
    ЗАПРЕЩЕНО:
    
    - from app.database import ...
    
    - Сначала проверь project_structure,
      потом создавай imports
    - Запрещено дублировать импорты

    - Один и тот же import
      нельзя повторять несколько раз

    - Если библиотека импортируется
      в коде,
      dependency ОБЯЗАНА
      присутствовать
      в requirements.txt

    Примеры:

    - import gspread → gspread

    - from dotenv import ... →
      python-dotenv

    - from telegram.ext import ... →
      python-telegram-bot

    - from oauth2client.service_account import ... →
      oauth2client

    - Не удаляй dependencies,
      указанные architect
      в architecture.requirements

    - Все зависимости из:
      architecture.requirements
      ОБЯЗАНЫ присутствовать
      в requirements.txt

    - Не удаляй зависимости
      из requirements.txt,
      если они используются
      в импортах

    Обязательные файлы:

    - app/main.py
    - requirements.txt

    - Используй многофайловую
      архитектуру

    - Используй только существующие
      пакеты PyPI

    - Используй современные
      версии библиотек

    - Проверяй совместимость кода
      с современными версиями пакетов

    - Если используется async def main,
      запуск ОБЯЗАН выполняться через:

      asyncio.run(main())

    Запрещено:

    - main()
    - await main()
      вне async context

    Для async main:

    - используй asyncio.run(main())

    - внутри async main
      используй:

      await application.initialize()
      await application.start()
      await application.updater.start_polling()

    - Не используй
      application.run_polling()
      внутри async def main

    Для python-telegram-bot >= 20:

    - используй Application
    - используй ApplicationBuilder
    - используй CommandHandler
    - используй MessageHandler
    - используй filters

    ЗАПРЕЩЕНО использовать:

    - Updater
    - Dispatcher
    - Filters
    - use_context

    Для aiogram 3:

    - используй Router

    - не используй
      executor.start_polling

    - не используй
      Dispatcher(bot)

    - Не добавляй стандартные
      модули Python
      в requirements.txt

    Примеры stdlib модулей:

    - os
    - sys
    - json
    - sqlite3
    - pathlib
    - argparse
    - datetime
    - asyncio
    - typing

    - Используй os.getenv()
      для секретов

    - Каждый файл ОБЯЗАН
      использовать ключ:
      "path"

    Пример:

    {{
        "path": "app/main.py",
        "content": "..."
    }}

    Запрещено использовать:

    - name
    - filename
    - file

    - Не используй markdown

    - Не добавляй пояснения

    - Корневой JSON ОБЯЗАН
      содержать только ключ:

      "files"

    - Запрещено возвращать:

    {{
        "path": ...
    }}

    - Каждый файл должен
      находиться внутри
      массива "files"

    - JSON должен быть
      полностью закрыт

    - Не обрезай конец JSON

    - Перед отправкой ответа
      проверь что JSON
      полностью закрыт

    - Все объекты files
      должны быть закрыты }}

    - Массив files
      должен быть закрыт ]

    - Корневой объект
      должен быть закрыт }}

    - Ответ должен завершаться:

      - закрытием массива files
      - закрытием корневого объекта

    Формат ответа:

    {{
        "files": [
            {{
                "path": "app/main.py",
                "content": "..."
            }}
        ]
    }}

    Верни только JSON.
    """

    @staticmethod
    def fix_prompt(
            task: str = "",
            architecture: str = "",
            error: str = "",
            previous_code: str = "",
            broken_file: str = "",
            review: str = "",
            knowledge="",
            missing_files=None
    ) -> str:
        if missing_files is None:
            missing_files = []

        return f"""
    Исправь ТОЛЬКО указанные ошибки.

    PATCH MODE АКТИВЕН.
    
    Правила PATCH MODE:
    
    - Запрещено пересоздавать проект
    - Запрещено изменять архитектуру
    - Запрещено удалять файлы
    - Запрещено изменять рабочие файлы
    - Разрешено изменять ТОЛЬКО:
      - сломанные файлы
      - отсутствующие файлы
      - requirements.txt
    
    - Если ошибка говорит:
      "Отсутствует файл"
      создавай ТОЛЬКО отсутствующий файл
    
    - Если ошибка связана с import:
      исправляй ТОЛЬКО import
    
    - Если ошибка связана с dependency:
      исправляй ТОЛЬКО requirements.txt
    
    - Не создавай новые директории
      если их нет в architecture
    
    - Не создавай новые файлы
      если их нет в architecture
    
    - Ответ должен содержать
      ТОЛЬКО изменённые файлы
    
    - Не возвращай весь проект

    ИСХОДНАЯ ЗАДАЧА:

    {task}

    АРХИТЕКТУРА ПРОЕКТА:

    {architecture}

    RUNTIME ERROR:

    {error}
    
    BROKEN FILE:

    {broken_file}
    
    QA REVIEW:

    {review}

    ОТСУТСТВУЮЩИЕ ФАЙЛЫ:

    {missing_files}

    СЛОМАННЫЙ ФАЙЛ:

    {previous_code}

    ПРАВИЛА КОМАНДЫ:

    {knowledge}

    КРИТИЧЕСКИЕ ПРАВИЛА:

    - Это PATCH MODE

    - Запрещено создавать
      новый проект с нуля

    - Запрещено изменять
      тип проекта

    - Если проект:
      telegram bot

      ЗАПРЕЩЕНО:

      - FastAPI
      - Flask
      - Django

    - Сохраняй архитектуру проекта

    - Исправляй ТОЛЬКО
      проблемные файлы

    - Не переписывай
      весь проект

    - Не удаляй файлы

    - Не удаляй imports

    - Не удаляй requirements.txt

    - Не удаляй app/main.py

    - Не изменяй path файлов

    - Используй ТОЛЬКО файлы
      из architecture.project_structure

    - Перед созданием import
      ОБЯЗАТЕЛЬНО проверь,
      существует ли файл
      в project_structure

    - Запрещено создавать imports
      несуществующих файлов

    - Если missing_files не пустой,
      ОБЯЗАТЕЛЬНО создай
      каждый missing file

    - Если для missing file
      нет логики,
      создай minimal stub

    Пример stub:

    {{
        "path": "app/api/telegram_api.py",
        "content": "class TelegramApi:\\n    pass"
    }}

    - Для __init__.py
      разрешён пустой content

    - Каждый file ОБЯЗАН содержать:

      - path
      - content

    - Любые другие ключи
      запрещены

    - Внутри files разрешены
      ТОЛЬКО:

      - path
      - content

    - Верни ТОЛЬКО JSON

    Формат ответа:

    {{
        "files": [
            {{
                "path": "...",
                "content": "..."
            }}
        ]
    }}
    """
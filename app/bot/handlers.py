from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from app.db.base import async_session
from app.services.request_service import RequestService
from app.core.config import settings

async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Отправь описание своей заявки, и я её сохраню."
    )


async def help_handler(message: types.Message):
    await message.answer(
        "Отправь текст заявки, и мы её обработаем.\nКоманды:\n/start - начать\n/help - помощь"
    )


async def request_handler(message: types.Message):
    description = message.text.strip()
    if not description:
        await message.answer("Пожалуйста, отправь текст заявки.")
        return

    async with async_session() as session:
        request = await RequestService.create_request(
            session=session,
            telegram_id=message.from_user.id,
            description=description,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
    await message.answer(
        f"Заявка принята! Номер заявки: {request.id}", parse_mode=ParseMode.HTML
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, Command("start"))
    dp.register_message_handler(help_handler, Command("help"))
    dp.register_message_handler(request_handler)
from aiogram import Bot, Dispatcher
from app.core.config import settings

bot = Bot(token=settings.bot_token, parse_mode="HTML")
dp = Dispatcher(bot)

from app.bot.handlers import register_handlers
register_handlers(dp)
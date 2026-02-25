import asyncio
import logging
import os

from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from handlers import schedule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    token = os.environ.get('BOT_TOKEN')
    if not token:
        raise ValueError('BOT_TOKEN env var required')

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await bot.set_my_commands([
        BotCommand(command='today', description='Расписание на сегодня'),
    ])

    dp.include_router(schedule.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

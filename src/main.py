from aiogram import Dispatcher, Bot
from src.utils import settings
from src.handlers import router
from src.db import Database
import asyncio

async def main():
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher()

    db = Database(settings.db.dsn)
    await db.connect()
    dp["db"] = db

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()

if __name__ == '__main__':
    asyncio.run(main())

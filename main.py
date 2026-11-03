
import asyncio
import logging
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage


from src.handlers import router as handlers_router

BOT_TOKEN = "8699853215:AAFzdKLYTHpxytuM4l-Aw2AhPWmNGLPR8f4"

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(handlers_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


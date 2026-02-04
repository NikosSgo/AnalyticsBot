from aiogram import Router, F
from aiogram.types import Message

from src.llm import ask_llm
from src.utils import logger

logger = logger.bind(module="handlers")
router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    logger.info(f"Команда /start от user_id={message.from_user.id}")
    await message.answer("Привет! Я бот и ты можешь задать мне вопрос по видео аналитике.")


@router.message(F.text)
async def llm_handler(message: Message, db):
    user_id = message.from_user.id
    prompt = message.text

    logger.info(f"Запрос аналитики от {user_id}: '{prompt}'")

    try:
        result = await ask_llm(prompt, db)
        logger.info(f"Ответ пользователю {user_id}: '{str(result)}'")
        await message.answer(str(result))
    except Exception as e:
        logger.error(f"Ошибка обработки запроса {user_id}: {e}")
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")

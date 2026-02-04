import json
from typing import TYPE_CHECKING

from openai import AsyncClient

from src.utils import logger
from src.utils import settings
from .build_sql_and_params import build_sql_and_params
from .functions import FUNCTIONS
from .prompt import SYSTEM_PROMPT

logger = logger.bind(module="llm")

if TYPE_CHECKING:
    from src.db import Database


async def ask_llm(prompt: str, db: "Database"):
    logger.info(f"LLM запрос: '{prompt}'")

    async with AsyncClient(api_key=settings.llm.api_key, base_url=settings.llm.url) as client:
        try:
            response = await client.chat.completions.create(
                model=settings.llm.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                functions=FUNCTIONS,
                function_call="auto"
            )
        except Exception as e:
            logger.error(f"Ошибка LLM API: {e}")
            return "Извините, произошла ошибка при обращении к ИИ."

    message = response.choices[0].message
    logger.debug(f"LLM ответ: function_call={message.function_call is not None}")

    if message.function_call is not None:
        func_name = message.function_call.name
        args = message.function_call.arguments
        args_dict = json.loads(args) if args else {}

        logger.info(f"Вызов функции: {func_name}({args_dict})")

        sql, sql_params = build_sql_and_params(func_name, args_dict)
        logger.debug(f"SQL: {sql}\nParams: {sql_params}")

        try:
            result = await db.run_query(sql, sql_params)
            logger.info(f"SQL результат: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка SQL: {e}")
            return "Ошибка при выполнении запроса к базе данных."

    logger.info(f"LLM текст: '{message.content}'")
    return message.content

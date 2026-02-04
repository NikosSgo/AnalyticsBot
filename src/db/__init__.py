import time

import asyncpg

from src.utils import logger

logger = logger.bind(module="database")


class Database:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(self._dsn)

    async def close(self):
        if self.pool is not None:
            await self.pool.close()

    async def run_query(self, sql: str, sql_params: list):
        logger.debug(f"Выполнение SQL: {sql[:100]}... | params={sql_params}")
        start = time.time()

        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchval(sql, *sql_params)
                duration = time.time() - start
                logger.debug(f"SQL выполнено за {duration:.2f}ms | результат={result}")
                return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"SQL ошибка за {duration:.2f}ms: {e}")
            raise

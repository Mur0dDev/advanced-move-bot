from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # Table creation methods
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            full_name VARCHAR(255),
            username VARCHAR(255),
            language VARCHAR(10) DEFAULT 'en',
            role VARCHAR(50) DEFAULT 'viewer',
            special_role VARCHAR(255) DEFAULT NULL,
            status VARCHAR(20) DEFAULT 'active',
            date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            phone_number VARCHAR(20),
            email VARCHAR(255),
            additional_info JSON
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_bot_messages(self):
        sql = """
        CREATE TABLE IF NOT EXISTS bot_messages (
            id SERIAL PRIMARY KEY,
            key VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            language VARCHAR(10) NOT NULL DEFAULT 'en',
            UNIQUE (key, language)
        );
        """
        await self.execute(sql, execute=True)

    # User-specific methods
    async def add_user(self, telegram_id: int, full_name: str, username: str, language: str = "en",
                       role: str = "viewer", special_role: str = None):
        sql = """
        INSERT INTO users (telegram_id, full_name, username, language, role, special_role)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (telegram_id) DO NOTHING;
        """
        await self.execute(sql, telegram_id, full_name, username, language, role, special_role, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def update_user(self, telegram_id: int, **kwargs):
        if not kwargs:
            raise ValueError("No fields provided to update.")
        fields = ", ".join([f"{key} = ${i + 2}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE users SET {fields}, last_active = CURRENT_TIMESTAMP WHERE telegram_id = $1"
        await self.execute(sql, telegram_id, *kwargs.values(), execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

    # Bot messages methods
    async def get_message(self, key: str, language: str = 'en') -> str:
        query = """
        SELECT message 
        FROM bot_messages 
        WHERE key = $1 AND language = $2
        LIMIT 1;
        """
        message = await self.execute(query, key, language, fetchval=True)
        if not message and language != 'en':
            message = await self.execute(query, key, 'en', fetchval=True)
        return message or "Message not found."

    async def insert_bot_messages(self, messages: list):
        sql = """
        INSERT INTO bot_messages (key, message, language)
        VALUES ($1, $2, $3)
        ON CONFLICT (key, language) DO UPDATE
        SET message = EXCLUDED.message;
        """
        for message in messages:
            await self.execute(sql, *message, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())

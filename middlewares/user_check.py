from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db

class UserCheckMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id

        # Check if the user exists in the `users` table
        user = await db.select_user(telegram_id=user_id)

        if user:
            # User is registered, allow processing
            data['user'] = user
            return

        # Check if the user exists in the `unregistered_users` table
        unregistered_user = await db.select_unregistered_user(telegram_id=user_id)

        if unregistered_user:
            # User is unregistered, allow limited functionality
            data['unregistered_user'] = unregistered_user
            return

        # If user is not in either table, add them to `unregistered_users`
        await db.add_unregistered_user(
            telegram_id=user_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username
        )

        # Notify the user
        await message.answer(
            "🚫 You are not registered with the bot. Limited functionality is available."
        )
        return False

# -*- coding: utf-8 -*-
import asyncio
import sys
from utils.db_api.postgresql import Database

# Fix for Windows event loop issues
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def setup_database():
    db = Database()
    await db.create()

    try:
        # Create required tables
        await db.create_table_users()
        print("Table 'users' created successfully!")

        await db.create_table_bot_messages()
        print("Table 'bot_messages' created successfully!")

        await db.create_table_unregistered_users()
        print("Table 'unregistered_users' created successfully!")

        # Insert initial bot messages
        bot_messages = [
            (
            'welcome_message', '🌟 Welcome to the MoveMeGroup Bot! 🚛\\n✨ Please select an option below to get started:',
            'en'),
            ('welcome_message',
             '🌟 MoveMeGroup Botiga xush kelibsiz! 🚛\\n✨ Boshlash uchun quyidagi variantlardan birini tanlang:', 'uz'),
            ('welcome_message',
             '🌟 Добро пожаловать в MoveMeGroup Bot! 🚛\\n✨ Выберите один из вариантов ниже, чтобы начать:', 'ru'),
            ('about_us',
             '🌟 Your Trusted Logistics Partner 🌟\\n\\nAt MoveMeGroup, we specialize in delivering innovative and efficient logistics solutions tailored to the needs of modern businesses. With a commitment to excellence, reliability, and customer satisfaction, we go the extra mile to ensure your goods reach their destination on time, every time.',
             'en'),
            ('about_us',
             '🌟 Ishonchli Logistika Hamkoringiz 🌟\\n\\nMoveMeGroup kompaniyasi innovatsion va samarali logistika yechimlarini taqdim etishga ixtisoslashgan.',
             'uz'),
            ('about_us',
             '🌟 Ваш надежный логистический партнер 🌟\\n\\nВ MoveMeGroup мы специализируемся на предоставлении инновационных и эффективных логистических решений.',
             'ru')
        ]
        await db.insert_bot_messages(bot_messages)
        print("Bot messages inserted successfully!")

        # Insert a sample user
        await db.add_user(
            telegram_id=7262828142,
            full_name="Milton Sullivan",
            username="miltonmoveme",
            language="en",
            role="admin",
            special_role=None
        )
        print("Sample user inserted successfully!")

    except Exception as e:
        print(f"Error setting up database: {e}")


# if __name__ == "__main__":
#     asyncio.run(setup_database())

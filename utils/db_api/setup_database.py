# -*- coding: utf-8 -*-
import asyncio
import sys
from utils.db_api.postgresql import Database  # Import your Database class

# Fix for Windows event loop issues
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def setup_database():
    db = Database()
    await db.create()  # Use the existing `create` function to establish the connection

    # SQL queries
    create_table_query = """
    CREATE TABLE IF NOT EXISTS bot_messages (
        id SERIAL PRIMARY KEY,
        key VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        language VARCHAR(10) NOT NULL DEFAULT 'en',
        UNIQUE (key, language)
    );
    """

    insert_welcome_message_query = """
    INSERT INTO bot_messages (key, message, language)
    VALUES 
        ('welcome_message', '🌟 Welcome to the MoveMeGroup Bot! 🚛\\n✨ Please select an option below to get started:', 'en'),
        ('welcome_message', '🌟 MoveMeGroup Botiga xush kelibsiz! 🚛\\n✨ Boshlash uchun quyidagi variantlardan birini tanlang:', 'uz'),
        ('welcome_message', '🌟 Добро пожаловать в MoveMeGroup Bot! 🚛\\n✨ Выберите один из вариантов ниже, чтобы начать:', 'ru')
    ON CONFLICT (key, language)
    DO NOTHING;
    """

    insert_about_us_query = """
    INSERT INTO bot_messages (key, message, language)
    VALUES 
        ('about_us', 
        '🌟 Your Trusted Logistics Partner 🌟\\n\\nAt MoveMeGroup, we specialize in delivering innovative and efficient logistics solutions tailored to the needs of modern businesses. With a commitment to excellence, reliability, and customer satisfaction, we go the extra mile to ensure your goods reach their destination on time, every time.\\n\\n🚛 What We Do:\\n- Freight Management: Seamlessly coordinate and transport your goods across the country.\\n- Dedicated Support: A professional team ready to assist with every aspect of your logistics needs.\\n- Innovative Solutions: Leveraging the latest technology to streamline operations and provide real-time updates.\\n\\n🌐 Our Mission:\\nTo empower businesses by simplifying logistics, reducing costs, and enhancing supply chain efficiency. We aim to set the standard for trust, transparency, and excellence in the transportation industry.\\n\\n💼 Why Choose MoveMeGroup?\\n- Experienced Team: Skilled professionals dedicated to solving your logistics challenges.\\n- Customer-Centric Approach: Your success is our priority.\\n- Scalability: Flexible solutions that grow with your business.\\n\\n🚀 Let us take the hassle out of logistics so you can focus on what matters most—your business. Welcome to the MoveMeGroup family!',
        'en'),
        ('about_us', 
        '🌟 Ishonchli Logistika Hamkoringiz 🌟\\n\\nMoveMeGroup kompaniyasi innovatsion va samarali logistika yechimlarini taqdim etishga ixtisoslashgan. Mukammallik, ishonchlilik va mijozlar mamnuniyatiga sodiq holda, biz sizning yuklaringizni o‘z vaqtida yetkazib berishni ta’minlash uchun qo‘limizdan kelgan barcha ishni qilamiz.\\n\\n🚛 Bizning Faoliyatimiz:\\n- Yuklarni boshqarish: Yuklaringizni butun mamlakat bo‘ylab muvofiqlashtirish va tashish.\\n- Yordamchi jamoa: Logistika ehtiyojlaringizning har bir bosqichida yordam berishga tayyor professional jamoa.\\n- Innovatsion Yechimlar: Operatsiyalarni soddalashtirish va real vaqt yangilanishlarini taqdim etish uchun eng so‘nggi texnologiyalardan foydalanish.\\n\\n🌐 Bizning Missiyamiz:\\nBizneslarni logistikani soddalashtirish, xarajatlarni kamaytirish va ta’minot zanjiri samaradorligini oshirish orqali rivojlantirish. Biz ishonch, shaffoflik va mukammallik tamoyillari asosida ish yuritamiz.\\n\\n💼 Nega MoveMeGroupni Tanlash kerak?\\n- Tajribali Jamoa: Logistika muammolarini hal qilishga bag‘ishlangan mutaxassislar.\\n- Mijozga Yo‘naltirilgan Yondashuv: Sizning muvaffaqiyatingiz - bizning ustuvorligimiz.\\n- Moslashuvchanlik: Biznesingiz o‘sishiga moslashuvchi yechimlar.\\n\\n🚀 Logistikadan qiyinchilikni olib tashlaymiz, siz esa eng muhim narsalarga e’tiboringizni qarata olasiz. MoveMeGroup oilasiga xush kelibsiz!',
        'uz'),
        ('about_us', 
        '🌟 Ваш надежный логистический партнер 🌟\\n\\nВ MoveMeGroup мы специализируемся на предоставлении инновационных и эффективных логистических решений, адаптированных к потребностям современных предприятий. Придерживаясь принципов совершенства, надежности и удовлетворенности клиентов, мы делаем все возможное, чтобы ваши грузы доставлялись вовремя.\\n\\n🚛 Что мы предлагаем:\\n- Управление грузоперевозками: Координация и транспортировка ваших грузов по всей стране.\\n- Посвященная поддержка: Профессиональная команда, готовая помочь на каждом этапе ваших логистических потребностей.\\n- Инновационные решения: Использование новейших технологий для оптимизации операций и предоставления обновлений в реальном времени.\\n\\n🌐 Наша миссия:\\nПоддерживать бизнес, упрощая логистику, снижая издержки и повышая эффективность цепочки поставок. Мы стремимся установить стандарты доверия, прозрачности и совершенства в транспортной отрасли.\\n\\n💼 Почему выбрать MoveMeGroup?\\n- Опытная команда: Квалифицированные специалисты, посвященные решению ваших логистических задач.\\n- Клиентоориентированный подход: Ваш успех — наш приоритет.\\n- Масштабируемость: Гибкие решения, которые растут вместе с вашим бизнесом.\\n\\n🚀 Мы берем на себя заботу о логистике, чтобы вы могли сосредоточиться на самом важном. Добро пожаловать в семью MoveMeGroup!',
    'ru')
    ON CONFLICT (key, language)
    DO UPDATE
    SET message = EXCLUDED.message;
    """

    try:
        # Create table
        await db.execute(create_table_query, execute=True)
        print("Table 'bot_messages' created successfully!")

        # Insert welcome messages
        await db.execute(insert_welcome_message_query, execute=True)
        print("Welcome messages inserted successfully!")

        # Insert About Us messages
        await db.execute(insert_about_us_query, execute=True)
        print("About Us messages inserted successfully!")

    except Exception as e:
        print(f"Error setting up database: {e}")


# if __name__ == "__main__":
#     asyncio.run(setup_database())

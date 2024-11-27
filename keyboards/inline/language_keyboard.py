from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_language_en"),
            InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data="set_language_uz"),
            InlineKeyboardButton(text="🇷🇺 Russian", callback_data="set_language_ru")
        ],
        [
            InlineKeyboardButton(text="❌ Close", callback_data="close_settings")
        ]
    ])

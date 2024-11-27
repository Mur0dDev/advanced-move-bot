from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Create buttons
start_button = KeyboardButton("🚀 Get Started")
settings_button = KeyboardButton("🛠️ Adjust Settings")
about_button = KeyboardButton("📝 About Us")

# Create keyboard
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(start_button).add(settings_button).add(about_button)
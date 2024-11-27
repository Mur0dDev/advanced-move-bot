from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from keyboards.default.main_menu import main_menu
from states.user_state import UserState
from keyboards.inline.language_keyboard import get_language_keyboard

@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message, state: FSMContext):
    await message.delete()

    # Default user language (you can fetch this dynamically later)
    user_language = 'en'

    # Fetch the welcome message and replace \n with actual newlines
    welcome_message = (await db.get_message(key="welcome_message", language=user_language)).replace("\\n", "\n")

    # Send the welcome message with the keyboard
    sent_message = await message.answer(
        welcome_message,
        reply_markup=main_menu
    )
    print(sent_message.message_id)

    # Set the state and store the message_id
    await UserState.stored_message_id.set()
    await state.update_data(
        stored_message_id=sent_message.message_id,
        chat_id=message.chat.id
    )

    # Debug: Log the chat_id and message_id
    print(f"Stored chat_id: {message.chat.id}, message_id: {sent_message.message_id}")


@dp.message_handler(lambda message: message.text == "🚀 Get Started", state=UserState.stored_message_id)
async def handle_start_button(message: types.Message, state: FSMContext):
    await message.delete()
    # Retrieve stored message_id and chat_id
    data = await state.get_data()
    message_id = data.get("stored_message_id")
    chat_id = data.get("chat_id")

    if message_id and chat_id:
        try:
            # Delete the old message
            await message.bot.delete_message(chat_id=chat_id, message_id=message_id)

            # Send a new message
            new_message = await message.answer(
                "You clicked 'Start'. The keyboard is now hidden.",
                reply_markup=types.ReplyKeyboardRemove()
            )

            # Update the state with the new message_id
            await state.update_data(stored_message_id=new_message.message_id)
        except Exception as e:
            print(f"Error while deleting/sending message: {e}")
            await message.answer("An error occurred. Please try again.")
    else:
        await message.answer("No editable message found. Please restart with /start.")

    # Finish the state
    await state.finish()


@dp.message_handler(lambda message: message.text == "🛠️ Adjust Settings", state=UserState.stored_message_id)
async def handle_settings_button(message: types.Message, state: FSMContext):
    await message.delete()  # Delete the user's message

    # Get stored message and chat IDs from state
    data = await state.get_data()
    message_id = data.get("stored_message_id")
    chat_id = data.get("chat_id")

    if message_id and chat_id:
        try:
            # Delete the previously stored message
            await message.bot.delete_message(chat_id=chat_id, message_id=message_id)

            # Send the new settings message with inline buttons for language selection
            new_message = await message.answer(
                "⚙️ Adjust your settings:\n\n🌐 Please select your preferred language:",
                reply_markup=get_language_keyboard()  # Inline keyboard for languages
            )
            await state.update_data(stored_message_id=new_message.message_id)
        except Exception as e:
            print(f"Error while deleting/sending message: {e}")
            await message.answer("An error occurred. Please try again.")
    else:
        await message.answer("No editable message found. Please restart with /start.")

    # Optionally, finish the current state
    await state.finish()


@dp.message_handler(lambda message: message.text == "📝 About Us", state=UserState.stored_message_id)
async def handle_about_button(message: types.Message, state: FSMContext):
    await message.delete()

    # Retrieve the user's preferred language (default to 'en')
    user_language = message.from_user.language_code or 'en'

    # Retrieve the "About Us" message from the database
    about_message = await db.get_message(key="about_us", language=user_language)

    # Replace escaped newlines
    about_message = about_message.replace("\\n\\n", "\n\n").replace("\\n", "\n")

    # Get stored message and chat IDs from state
    data = await state.get_data()
    message_id = data.get("stored_message_id")
    chat_id = data.get("chat_id")

    if message_id and chat_id:
        try:
            # Delete the previously stored message
            await message.bot.delete_message(chat_id=chat_id, message_id=message_id)

            # Send the clean "About Us" message
            new_message = await message.answer(
                about_message,
                reply_markup=types.ReplyKeyboardRemove()
            )

            # Update state with the new message ID
            await state.update_data(stored_message_id=new_message.message_id)
        except Exception as e:
            print(f"Error while deleting/sending message: {e}")
            await message.answer("An error occurred. Please try again.")
    else:
        await message.answer("No editable message found. Please restart with /start.")

    # Finish the current state
    await state.finish()

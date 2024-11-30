from utils.db_api.postgresql import Database

db = Database()

async def get_preferred_language(telegram_id: int) -> str:
    """
    Get the preferred language of a user from either 'users' or 'unregistered_users'.
    Returns the language code or 'en' (default) if the user is not found.
    """
    # Check in the 'users' table
    sql_users = "SELECT language FROM users WHERE telegram_id = $1;"
    language = await db.execute(sql_users, telegram_id, fetchval=True)

    if language:
        return language

    # Check in the 'unregistered_users' table
    sql_unregistered = "SELECT language FROM unregistered_users WHERE telegram_id = $1;"
    language = await db.execute(sql_unregistered, telegram_id, fetchval=True)

    return language or "en"  # Default to English if not found

async def update_preferred_language(telegram_id: int, language: str):
    """
    Update the preferred language of a user in either 'users' or 'unregistered_users'.
    Raises an exception if the user is not found in either table.
    """
    # Try updating in the 'users' table
    sql_users = "UPDATE users SET language = $1 WHERE telegram_id = $2;"
    result = await db.execute(sql_users, language, telegram_id, execute=True)

    if result and result.lower() == "update 0":  # No rows updated in 'users'
        # Try updating in the 'unregistered_users' table
        sql_unregistered = "UPDATE unregistered_users SET language = $1 WHERE telegram_id = $2;"
        result = await db.execute(sql_unregistered, language, telegram_id, execute=True)

    if result and result.lower() == "update 0":  # No rows updated in 'unregistered_users'
        raise ValueError("User not found in either 'users' or 'unregistered_users'.")

# this file handels all stuff on message

from config import active_users
from db_manager import exists_in_db
from user_class import User

async def handle_message(bot, message):
    if message.author.bot:
        return

    # Check if user is in active_users or the database
    if message.author.id not in active_users:
        print(message.author.id)
        user_data = exists_in_db(message.author.id)
        print(f"User data: {user_data}")
        if user_data:
            new_user = User(user_data[0])
            new_user.level = user_data[1]
            new_user.balance = user_data[2]
            active_users[message.author.id] = new_user

    # Process commands if message contains any
    await bot.process_commands(message)
# this file handels all stuff on message

from config import active_users
from general_functions import add_to_active_users
from db_manager import exists_in_db
from user_class import User

async def handle_message(bot, message):
    if message.author.bot:
        print("bot message detected")
        return

    # Check if user is in active_users or the database
    if message.author.id not in active_users:
        print(message.author.id)
        add_to_active_users(message.author)
    
    # if the messgae was a command, dont do anything further
    if message.content[0] == ".":
        await bot.process_commands(message)
        return

    # xp handling
    try:
        print(active_users)
        active_users.get(message.author.id).xp += 1
        if active_users.get(message.author.id).check_levelup():
            print("Successfully leveled up!")
            # for some reason this doenst send?
            # ask gpt
            await message.channel.send(f"Congrats! <@{message.author.id}> you leveled up to level {active_users[message.author.id].level}")
        else:
            print("DEBUG: no level up ")
    except KeyError:
        print(f"User not in active database")

    # Process commands if message contains any
    await bot.process_commands(message)
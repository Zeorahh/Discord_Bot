# where commonly used functions will be stored

import discord
from db_manager import exists_in_db
from config import active_users
from user_class import User 

def add_to_active_users(member : discord.Member):
    if member.id not in active_users:
        print(member.id)
        user_data = exists_in_db(member.id)
        print(f"User data: {user_data}")
        if user_data:
            new_user = User(user_data[0])
            new_user.level = user_data[1]
            new_user.balance = user_data[2]
            new_user.xp = user_data[3]
            new_user.luck = user_data[4]
            new_user.money_multiplier = user_data[5]
            active_users[member.id] = new_user

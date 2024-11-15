## this file takes care of bot tasks (automated stuff)
from discord.ext import tasks
from config import active_users
from db_manager import update_all_users
import os
import datetime
import shutil

def start_scheduled_tasks(bot):

    # saves all data every 15 minutes
    @tasks.loop(minutes=15)
    async def update_db():
        print("Updating database")
        update_all_users(active_users)
        active_users.clear()
        print("Database updated")


    update_db.start()
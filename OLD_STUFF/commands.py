## this file is incharge of the bot commands
from db_manager import exists_in_db, register_new_user, update_all_users, initialize_db
from user_class import User
from config import active_users, db_connection
from general_functions import add_to_active_users
from discord.ext import commands
import random
import discord
import os
import sqlite3
import asyncio



# a list of all comands the bot has
def register_commands(bot):






    # @bot.command(name = "delete_database")
    # @commands.is_owner()
    # async def delete_database(ctx, confirmation : str = None):
    #     try:
    #         if confirmation!= "CONFIRM_DELETE":
    #             print('Attempted databsae deletion, did not confirm with "CONFIRM_DELETE"')
    #         else:
    #             print("Attempting databsae deletion...")
    #             db_path = "MAIN_USER_DATABSE.db"
    #             if os.path.exists(db_path):
    #                 db_connection.close()
    #                 print("Datbase found, comending deletion")
    #                 os.remove(db_path)
    #                 print("Database succesfully deleted")
                    
    #                                 # Reopen the database after deletion and recreation
    #                 global db_connection  # Ensure we update the global connection
    #                 db_connection = sqlite3.connect("path_to_your_database.db")
    #                 initialize_db()
    #                 print("New database created!")
    #             else:
    #                 print("Datbase not found, cannot delete")
                
    #     except Exception as e:
    #         print(f'An error occurred: {e}')
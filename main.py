## Discord bot
# this is the main file that actually runs the bot

# imports
import discord
from discord.ext import commands
from db_manager import initialize_db
from commands import register_commands
from message_handler import handle_message
import os
from dotenv import load_dotenv

# loads token from environment variable
load_dotenv()

# intents
# these give the bot permission to do things
intents = discord.Intents.default()
intents.message_content = True # can read messages
intents.members = True # can look at members

# setting up the bot and the prefix 
bot = commands.Bot(command_prefix="`", intents = intents)

# events that trigger on the bot startup
@bot.event
async def on_ready():
    print("Bot has successfully started")
    initialize_db() # makes sure the database is up and running

# this lest the bot use all the things in mesage handler
@bot.event
async def on_message(message):
    await handle_message(bot, message)

register_commands(bot) # this enables all the commands in commands.py 


bot.run(os.getenv("DISCORD_TOKEN"))
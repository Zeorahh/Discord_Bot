## Discord bot
# this is the main file that actually runs the bot

# imports
import discord
from discord.ext import commands
from db_manager import initialize_db
from message_handler import handle_message
import os
from dotenv import load_dotenv
from tasks import start_scheduled_tasks

# imports the files from the commands folder
from commands import admin_commands, debug_commands, regular_commands

# loads token from environment variable
load_dotenv()

# intents
# these give the bot permission to do things
intents = discord.Intents.default()
intents.message_content = True # can read messages
intents.members = True # can look at members

# setting up the bot and the prefix 
bot = commands.Bot(command_prefix=".", intents = intents)

# loads all the commands from the files
# if you add new command files
# you need to update this here
admin_commands.setup_admin(bot)
debug_commands.setup_debug(bot)
regular_commands.setup_regular(bot)

# events that trigger on the bot startup
@bot.event
async def on_ready():
    print("Bot has successfully started")
    initialize_db() # makes sure the database is up and running
    start_scheduled_tasks(bot)
    channel_id = 1300568651694608434
    channel = bot.get_channel(channel_id)
    if channel is not None:
        await channel.send(f"On with a ping of {round(bot.latency * 1000)}ms")
    else:
        print("Channel not found")

# this lest the bot use all the things in mesage handler
@bot.event
async def on_message(message):
    await handle_message(bot, message)

bot.run(os.getenv("DISCORD_TOKEN"))
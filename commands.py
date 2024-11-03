## this file is incharge of the bot commands
from db_manager import exists_in_db, register_new_user
from user_class import User
from config import active_users, db_connection
from discord.ext import commands

# a list of all comands the bot has
def register_commands(bot):

    #shutdown command
    @bot.command(name='shutdown', aliases=["end"])
    @commands.is_owner()  # This decorator ensures that only the owner can use this command
    async def shutdown(ctx):
        await ctx.send("Shutting down...")
        await bot.close()



    # register command, creates a new user if they don't exist in the database
    @bot.command(name='register',aliases=["reg"])
    async def register(ctx):
        # checks if a user is already registered
        user = exists_in_db(ctx.author.id)
        if user:
            await ctx.reply(f"{ctx.author.display_name}, you are already registered.")
            return
        
        # registers the user if they don't exist
        if register_new_user(ctx.author): # adds the user to the database
            await ctx.reply(f"{ctx.author.display_name}, you have successfully registered.")
        else: 
            await ctx.reply(f"{ctx.author.display_name}, there was an issue with registering you.")

    # this is for debugging purposes
    # simply shows all the currently registered users
    @bot.command(name="show_db")
    async def show_db(ctx) -> None:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if not users:
            await ctx.reply("No users in the database.")
            return
        for user in users:
            await ctx.send(f"ID: {user[0]}, Level: {user[1]}, Balance: {user[2]}")
    
    # a command for admin purposes
    # allows you to freely change money


    # command that pings the server
    @bot.command(name="ping")

    async def ping(ctx):
        await ctx.send(f"Latency: {round(bot.latency * 1000)}ms")
    
    @bot.command(name="invite")
    async def invite(ctx):
        await ctx.send(f"Invite link: {bot.invite_url}")
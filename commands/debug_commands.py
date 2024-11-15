## this file takes care of debug commands, not something that regular users should ever touch

import discord
from discord.ext import commands
from config import active_users, db_connection
import asyncio

def setup_debug(bot):
    # multi message MM
    @bot.command(name = "mm")
    async def mm(ctx):
        print("mm started")
        await ctx.send("Right or left?")
        # somehow get next message and do stuff off that

        def checkb(m):
            return m.author == ctx.author  and (m.content.lower() == "left" or m.content.lower() == "right")
        
        try:
            print("trying")
            msg = await bot.wait_for("message",check=checkb, timeout = 30)
            if msg.content.lower() == "right":
                await ctx.send("You chose right! You're a winner!")
            elif msg.content.lower() == "left":
                await ctx.send("You chose left! You're a loser!")
            else:
                await ctx.send("Invalid input. Please choose either 'left' or 'right'.")
        except asyncio.TimeoutError:
            await ctx.reply("took to long...")

    @bot.command(name="activeusers")
    async def activeusers(ctx):
        print("DEBUG: ALL CURRENT USERS")
        for user in active_users:
            print(f"DEBUG:{user}")

    # command that pings the server
    @bot.command(name="ping")

    async def ping(ctx):
        await ctx.send(f"Latency: {round(bot.latency * 1000)}ms")
    
    
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
        # cycle through all the users in the database and show their stats
        for user in users:
            await ctx.send(f"ID: {user[0]}, Level: {user[1]}, Balance: {user[2]} xp: {user[3]} Luck: {user[4]} MoneyMult {user[5]}")

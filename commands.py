## this file is incharge of the bot commands
from db_manager import exists_in_db, register_new_user, update_all_users
from user_class import User
from config import active_users, db_connection
from discord.ext import commands
import random
import discord

def on_mention(member : discord.Member):
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
            active_users[member.id] = new_user

# a list of all comands the bot has
def register_commands(bot):

    #shutdown command
    @bot.command(name='shutdown', aliases=["end"])
    @commands.is_owner()  # This decorator ensures that only the owner can use this command
    async def shutdown(ctx):
        await ctx.send("Saving all data...")
        update_all_users(active_users)
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
    @bot.command(name="changemoney")
    @commands.is_owner()
    async def changemoney(ctx, amount: float, member : discord.Member = None):
        if member is None:
            member = ctx.author
        on_mention(member)
        target_user : User = active_users[member.id]
        if target_user is None:
            await ctx.reply(f"Error: {member.display_name} is not registered.")
            return
        target_user.balance = round(target_user.balance + amount,2)
        await ctx.send(f"You have changed  ${amount} to {member.display_name}'s account.")
        active_users[member.id] = target_user

    # command that pings the server
    @bot.command(name="ping")

    async def ping(ctx):
        await ctx.send(f"Latency: {round(bot.latency * 1000)}ms")
    
    @bot.command(name="flip")
    async def flip(ctx,gamble : float = None,  coin: str = None):
        if gamble is None or gamble <= 0:
            await ctx.reply("Error: you must bet more then $0.01")
            return
        if coin is None:
            coin = "heads"
        current_user : User = active_users[ctx.author.id]
        if gamble > current_user.balance:
            await ctx.reply("Error: you don't have enough money")
            return
        roll = random.uniform(0,100) * current_user.luck
        gamble = round(gamble,2)
        old_bal : float = round(current_user.balance,2)
        if 50 < roll:
            current_user.balance = round(current_user.balance + gamble,2)
            await ctx.send(f"You landed on {coin}! you won ${gamble}!")
        else:
            if coin == "heads":
                coin = "tails"
            elif coin == "tails":
                coin = "heads"
            current_user.balance = round(current_user.balance - gamble,2)
            await ctx.send(f"You landed on {coin}... you lost ${gamble}!")
        
        embed = discord.Embed(title = ctx.author.display_name)
        embed.add_field(name = "", value = f"${old_bal} -> {current_user.balance}")
        await ctx.reply(embed=embed)

    @bot.command(name="stats", aliases = ["status","s"])
    async def stats(ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        on_mention(member)
        user : User = active_users.get(member.id)
        if user is None:
            await ctx.reply(f"{member.display_name}, you need to register first.")
            return
        embed = discord.Embed(title = member.display_name)
        embed.add_field(name = "Level", value = user.level)
        embed.add_field(name = "Balance", value = f"${user.balance}")
        await ctx.reply(embed=embed)
    
    # removes someone from the database
    # mostly for admin uses
    @bot.command(name="remove")
    @commands.is_owner()
    async def remove(ctx, member : discord.Member = None):
        user = exists_in_db(member.id)
        if user:
            cursor = db_connection.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (member.id,))
            db_connection.commit()
            if member.id in active_users.keys():
                del active_users[member.id]
            await ctx.send(f"User {member.display_name} removed from the database.")
        else:
            await ctx.reply(f"{member.display_name} was not in the database.")

    # slots!
    @bot.command(name="slots")
    async def slots(ctx, bet : float = None):
        print("Slots")
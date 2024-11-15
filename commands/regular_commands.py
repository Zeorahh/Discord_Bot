# this file takes care of all the commands normal users can use


import discord
from discord.ext import commands
from user_class import User
from db_manager import exists_in_db, register_new_user
from config import active_users
from general_functions import add_to_active_users
import random



def setup_regular(bot):
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
    
    @bot.command(name="flip")
    async def flip(ctx,gamble : float = None,  coin: str = None):
        if gamble is None or gamble <= 0:
            await ctx.reply("Error: you must bet at least one cent")
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
        add_to_active_users(member)
        user : User = active_users.get(member.id)
        if user is None:
            await ctx.reply(f"{member.display_name}, you need to register first.")
            return
        embed = discord.Embed(
            color=member.color)
        embed.set_author(
            name = member.display_name,
            icon_url=member.display_avatar.url
        )
        required_xp = user.get_required_xp()
        embed.add_field(name = "Stats: ",value=f"Level: {user.level}\nXP: {user.xp}/{required_xp}\nBalance: ${user.balance:.2f}\nLuck: {user.luck*100}%")
        await ctx.reply(embed=embed)
    
    @bot.command(name="slots", description="rolls a slot, takes $10 per use")
    async def slots(ctx, times_spun : int = 1):
        if times_spun <= 0:
            await ctx.reply("Error: you must spin at least once.")
            return
        if times_spun * 10 > active_users[ctx.author.id].balance:
            await ctx.reply("Error: you don't have enough money to spin.")
            return
        current_user : User = active_users[ctx.author.id]
        current_user.balance -= times_spun * 10
        await ctx.send(f"You spent ${times_spun * 10} on slots.")
        luck = current_user.luck
        total_won : float = 0.0
        for _ in range(times_spun):
            array = [random.randint(1, 10) for _ in range(10)]
            print("Array:", array)
            # Initialize variables to keep track of the longest consecutive count
            temp_longest_concurrent = 0
            longest_concurrent = 0

            for j in range(1, len(array)):
                # Check if the current element is the same as the previous one
                if array[j] == array[j - 1]:
                    temp_longest_concurrent += 1  # Increase the current streak
                else:
                    # Update longest streak if current streak is longer
                    if temp_longest_concurrent > longest_concurrent:
                        longest_concurrent = temp_longest_concurrent
                    temp_longest_concurrent = 1  # Reset current streak

            # Final check for the longest streak
            if temp_longest_concurrent > longest_concurrent:
                longest_concurrent = temp_longest_concurrent
            if random.random() < (luck - 1):
                print("You got lucky!")
                longest_concurrent += 1
            mega_jackpots = 0
            jackpots = 0
            wins = 0
            if longest_concurrent >= 6:
                mega_jackpots += 1
            if longest_concurrent >= 5:
                jackpots += 1
            elif longest_concurrent >= 3:
                wins += 1
            total_won += wins * 150 + jackpots * 2000 + mega_jackpots * 10000
        total_won = round(total_won,2)
        current_user.balance += total_won
        await ctx.send(f"You won ${total_won}!")
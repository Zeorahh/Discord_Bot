# this file takes care of all the commands normal users can use


import discord
from discord.ext import commands
from user_class import User
from db_manager import exists_in_db, register_new_user
from config import active_users
from general_functions import add_to_active_users
import random

# this is for the beg command 
from datetime import datetime, timedelta
user_beg_cooldown : dict = {}


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
    
    @bot.command(name="beg")
    async def beg(ctx):
        print("DEBUG: beg")
        current_user :User = active_users.get(ctx.author.id)
        if current_user is None:
            await ctx.reply(f"{ctx.author.display_name}, you need to register first.")
            return
        

        # timeing stuff 
        # most of this code is chatgpt as ive never used deltatime before
        last_beg_time = user_beg_cooldown.get(ctx.author.id) # checks if the user has any beg time
        if last_beg_time is not None: # if they begged before
            time_difference = datetime.now() - last_beg_time
            
            if time_difference < timedelta(hours=1):
                if ctx.author.guild_permissions.administrator:
                    await ctx.reply(f"admin perms abused...")
                else:
                    await ctx.reply(f"{ctx.author.display_name}, you can only beg once every hour.")
                    return
        
        # actually dealing with the money now
        luck = current_user.luck
        money_mult = current_user.money_multiplier

        # first roll to see if you even earn any money
        # should be around a 75% change normally
        chance_roll = random.random() * luck
        print(f"DEBUG: rolled a {chance_roll}")
        if chance_roll < 0.25:
            await ctx.reply("No one bothered to help you...")
        else:
            # second roll to see how much money you earn
            
            money_roll = round(random.random() * luck * 10 * money_mult,2)
            current_user.balance += money_roll
            await ctx.send(f"You recieved ${money_roll} from begging")
        
        # updating the cooldown
        user_beg_cooldown[ctx.author.id] = datetime.now()


    # give command, gives people money
    @bot.command(name = "give")
    async def give(ctx, member : discord.Member, amount : float):
        if member is None:
            await ctx.reply("you need to specify a user to give too")
            return
        if amount <= 0:
            await ctx.reply("Error: you must give a positive amount.")
            return
        add_to_active_users(member)
        # checks to see if both users are int he active users database
        author = active_users.get(ctx.author.id)
        if not author:
            await ctx.reply(f"{ctx.author.display_name}, you need to register first.")
            return
        recipient = active_users.get(member.id)
        if not recipient:
            await ctx.reply(f"{member.display_name} is not a registered member")
            return
        if author.balance < amount:
            await ctx.reply("Error: you don't have enough money.")
            return
        author.balance -= amount
        recipient.balance += amount

        embed = discord.Embed(title=f"{ctx.author.display_name} -> {member.display_name}")
        embed.add_field(name = "", value = f"${author.balance:.2f} -> ${recipient.balance:.2f}")
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
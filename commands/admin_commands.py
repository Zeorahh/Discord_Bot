## this file takes care of all admin only commands for easier sorting

import discord
from discord.ext import commands
from config import active_users, db_connection
from db_manager import update_all_users, exists_in_db
from general_functions import add_to_active_users
from user_class import User

def setup_admin(bot):
    
    #shutdown command
    @bot.command(name='shutdown', aliases=["end"])
    @commands.is_owner()  # This decorator ensures that only the owner can use this command
    async def shutdown(ctx):
        await ctx.send("Saving all data...")
        update_all_users(active_users)
        await ctx.send("Shutting down...")
        await bot.close()
        print("Bot shutdown...")

        # a command for admin purposes
    # allows you to freely change money
    @bot.command(name="changemoney")
    @commands.is_owner()
    async def changemoney(ctx, amount: float, member : discord.Member = None):

        # checks if a member was said, else it used the one who sent the message
        if member is None:
            member = ctx.author

        # on mention loads the desiered user into active_users  the same way 
        # someone gets added when they send a message
        add_to_active_users(member)

        # this gets the user from active_users by using their discord id as a key
        target_user : User = active_users[member.id]

        # if this is none, that means they were not in active_users
        if target_user is None:
            await ctx.reply(f"Error: {member.display_name} is not registered.")
            return
        
        # changes that users stats
        target_user.balance = round(target_user.balance + amount,2)
        await ctx.send(f"You have changed  ${amount} to {member.display_name}'s account.")

        # updates active users with the new data (might be unneded? not sure honesly)
        #active_users[member.id] = target_user

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

    # manually saves the database
    @bot.command(name="save")
    async def save(ctx):
        try:
            print("Updating database")
            update_all_users(active_users)
            active_users.clear()
            print("Database updated")
            await ctx.reply("Data succesfully saved!")
        except:
            await ctx.reply("An error occured when trying to save the data")
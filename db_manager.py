## file dealing with all the database connections 
from config import db_connection
from user_class import User
import discord

def initialize_db():
    cursor = db_connection.cursor()

    # this is creating the table for the database
    #  only creats it if it doenst exist
    # IMPORTANT NOTE:
    # changing the database requires changing all other functions that rely on posistons
    #
    #
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, -- 0 index
            level INTEGER DEFAULT 0, -- 1 index
            balance REAL DEFAULT 0.0, -- 2 index
            xp INTEGER DEFAULT 0, -- 3 index
            luck REAL DEFAULT 1.0 -- 4 index
        )
    ''')
    db_connection.commit()

# this checks if the user exists, and returns the user
def exists_in_db(user_id : int):
    cursor = db_connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()

# this is for registering a new user to the database
def register_new_user(member : discord.Member) -> bool:
    try:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO users (id) VALUES (?)",
            (member.id,)  # Set default values for level and balance
        )
        db_connection.commit()
        print(f"{member.id} : {member.display_name} successfully registered")
        return True
    except Exception as e:
        print(f"error registering user {member.id} : {member.name}")
        return False
    

# this cycles through all current users in active users and saves them to the database
def update_all_users(active_users : dict) -> None:
    cursor = db_connection.cursor()
    cursor.executemany("UPDATE users SET level = ?, balance = ? , xp = ?, luck = ?WHERE id = ?",
                       [(user.level, user.balance, user.xp, user.luck, user.user_id) for user in active_users.values()])
    db_connection.commit()
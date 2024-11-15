## this is a file that stores global variables
## 

import sqlite3


# this is the connection to the database
db_connection = sqlite3.connect("MAIN_USER_DATABSE.db")

# this is a dictionary to store the active users
# so the bot can access them faster
active_users : dict = {}


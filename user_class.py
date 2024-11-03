## this file contails the user class

class User:
    def __init__(self, user_id : int):

        # the important stuff dealing with user account
        self.user_id : int = user_id

        #stuff for dealing with level
        self.level : int = 1
        self.xp : int = 0
        
        # stuff for dealing with money
        self.balance : float = 0.0

        # other funny stats
        self.luck : float = 1
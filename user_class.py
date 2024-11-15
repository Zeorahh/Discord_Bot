## this file contails the user class

## TODO:
# figure out a way to make levels useful
# figure out a way to increase luck and money multiplier
# figure out other fun stuff to do
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
        self.luck : float = 1.0
        self.money_multiplier : float = 1.0
    
    def levelup(self):
        self.level += 1
        self.money_multiplier += 0.01
        if self.level%10 == 0:
            self.luck += 0.01
    def get_required_xp(self):
        return int(10 * (self.level ** (1+(self.level/100))))
    def check_levelup(self):
        print(f"XP: {self.xp}")
        print(f"Level: {self.level}")
        required_xp = self.get_required_xp()
        # calculates the required XP for the next level
        if self.xp >= required_xp:
            self.xp -= required_xp
            self.levelup()
            
            # todo:
            # figure out how to send a message through the discord bot
            # even though this is a class
            return True
        return False
    

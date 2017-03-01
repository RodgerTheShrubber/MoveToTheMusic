"""
This class represents a player -- there is one controller(game pad) per player, and one player profile per player
"""
from PlayerProfile import PlayerProfile
from Controller import Controller
from GameStats import GameStats


totalPlayers = 0
class Player(object):
    
    def __init__(self):
        global totalPlayers
        if totalPlayers < 2:
            totalPlayers += 1
        self.profile = PlayerProfile()
        self.controller = Controller(totalPlayers)
        self.currentGameStats = GameStats()
        
    def getName(self):
        return self.profile.getPlayerName()
    
    def getController(self):
        return self.controller
    
    def getProfile(self):
        return self.profile
    
    def getGameStats(self):
        return self.currentGameStats
    
    def setGameStats(self, stats):
        self.currentGameStats = stats
       
    def setProfile(self, pp):
        self.profile = pp
        
    
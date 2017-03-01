"""
    GameInfo holds pertinent information about the player and the game presently being played.
    It can be used to easily pass game data from one part of the program to another.
    It relies on the PlayerProfile class for saving data and GameProfile for other game
    settings persistent across sessions.
"""

"""
    Started 24 Feb by Jason Cisarano.  Created basic attributes and methods.  
    20 March -- added PlayerProfile, changed many internal variables to use PlayerProfile items
    27 March -- added getPlayerProfile method
    29 March -- added support for GameProfile, changed volumes to use GameProfile values
"""
from PlayerProfile import PlayerProfile
from GameSettings import GameSettings
from Player import Player

class GameInfo(object):
    """
       GameInfo holds pertinent information about the player and the game presently being played.
       It can be used to easily pass game data from one part of the program to another.
       It relies on the PlayerProfile class for saving data and GameProfile for other game
       settings persistent across sessions.
    """
    
    def __init__(self):
        self.__mode = "freeplay"
        self.__currentLevel = 1
        self.__currentSong = ""
        
        self.__gs = GameSettings()
        self.__players = [Player()]
        
    def getSettings(self):
        return self.__gs
    
    def getPlayers(self):
        return self.__players
    
    def getPlayer(self, playerNumber):
        return self.__players[playerNumber]
    
    def getCurrentLevel(self):
        return self.__currentLevel
        
    def getGameMode(self):
        "Possible types: freeplay or career"
        return self.__mode
    
    def getGameModeAsInt(self):
        """
           Returns value as int instead of string.
           freeplay = 0, career = 1
           Returns None in error case.
        """
        if self.getGameMode() == "freeplay":
            return 0
        elif self.getGameMode() == "career":
            return 1
        else:
            return None       
    
    def getNumPlayers(self):
        "currently only single player mode available"
        return len(self.__players)
      
    
    def getCurrentSong(self):
        return self.__currentSong
    
    
    def setSettings(self, gameSettings):
        self.__gs = gameSettings
    
    def setPlayers(self, players):
        self.__players = players
        
    def addNewPlayer(self, player):
        self.__players.append(player)
    
            
    def setCurrentLevel(self, number):
        self.__currentLevel = number
    
    def setCurrentSong(self, songTuple):
        """
           Requires a tuple: (song_title, \song_filename)
        """
        self.__currentSong = songTuple
            
    def setGameMode(self, m):
        """
           Accepts input as text or int
           0 == freeplay
           1 == career
        """
        if m=="freeplay" or m=="career":
            self.__mode=m
            return True
        elif m==0 or m==1:
            if m==0:
                self.__mode = "freeplay"
            elif m==1:
                self.__mode = "career"
        else:
            return False
            
    def setNumPlayers(self, numPlay):
        """
           Num of players as int 1 or 2.
        """
        if numPlay == 1 or numPlay == 2:
            self.__numPlayers=numPlay
            return True
        else:
            return False
    
        
        
    def __str__(self):
        return "%s is playing a %s-player %s game."%(self.getPlayerName(), self.__numPlayers, self.__mode)

   


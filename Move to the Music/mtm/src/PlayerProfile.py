"""
   PlayerProfile holds the player's statistics and game progress. Includes internal methods to store
   and retrieve player data based on user name.
   
   On creation of an account, the user can simply attempt to addNewPlayerName and
   PlayerProfile will check against the profiles.p file to verify the name doesn't
   exist and then add it if it does not.
   
   On loading an existing account, the user should create a new PlayerProfile object
   and then use addExistingPlayerName to set the name before attempting to load player data.
   
   PlayerProfile also has a method that loads the profiles.p file and returns all player names as a list.
"""

"""
   Started 16 March by Jason Cisarano.  Pickle retrieve not working yet--it seems to save fine, though.
   20 March -- completed save and load functions.  Added checking to avoid players' using existing names.
   Added error handling.
"""

import cPickle as pickle
import os
from FileLocations import FileLocations
fileLocs = FileLocations()

class PlayerIOError(Exception):
    """
       Custom error message for problems with loading and saving files
    """
    def __init__(self, message):
        self.__message = message
    def __str__(self):
        return repr(self.__message)

class PlayerProfile(object):
    fileLocs=FileLocations()
    ALPH_DICT = {
             "A":fileLocs.alphSounds+"\\menu_11_01.ogg", "B":fileLocs.alphSounds+"\\menu_11_02.ogg", "C":fileLocs.alphSounds+"\\menu_11_03.ogg",
             "D":fileLocs.alphSounds+"\\menu_11_04.ogg", "E":fileLocs.alphSounds+"\\menu_11_05.ogg", "F":fileLocs.alphSounds+"\\menu_11_06.ogg",
             "G":fileLocs.alphSounds+"\\menu_11_07.ogg", "H":fileLocs.alphSounds+"\\menu_11_08.ogg", "I":fileLocs.alphSounds+"\\menu_11_09.ogg",
             "J":fileLocs.alphSounds+"\\menu_11_10.ogg", "K":fileLocs.alphSounds+"\\menu_11_11.ogg", "L":fileLocs.alphSounds+"\\menu_11_12.ogg",
             "M":fileLocs.alphSounds+"\\menu_11_13.ogg", "N":fileLocs.alphSounds+"\\menu_11_14.ogg", "O":fileLocs.alphSounds+"\\menu_11_15.ogg",
             "P":fileLocs.alphSounds+"\\menu_11_16.ogg", "Q":fileLocs.alphSounds+"\\menu_11_17.ogg", "R":fileLocs.alphSounds+"\\menu_11_18.ogg",
             "S":fileLocs.alphSounds+"\\menu_11_19.ogg", "T":fileLocs.alphSounds+"\\menu_11_20.ogg", "U":fileLocs.alphSounds+"\\menu_11_21.ogg",
             "V":fileLocs.alphSounds+"\\menu_11_22.ogg", "W":fileLocs.alphSounds+"\\menu_11_23.ogg", "X":fileLocs.alphSounds+"\\menu_11_24.ogg",
             "Y":fileLocs.alphSounds+"\\menu_11_25.ogg", "Z":fileLocs.alphSounds+"\\menu_11_16.ogg", "-":fileLocs.alphSounds+"\\menu_11_27.ogg",
             "?":fileLocs.alphSounds+"\\menu_11_27.ogg"
             } 
    """
      PlayerProfile holds the player's statistics and game progress. Includes internal methods to store
      and retrieve player data based on user name.
   
      On creation of an account, the user can simply attempt to addNewPlayerName and
      PlayerProfile will check against the profiles.p file to verify the name doesn't
      exist and then add it if it does not.
   
      On loading an existing account, the user should create a new PlayerProfile object
      and then use addExistingPlayerName to set the name before attempting to load player data.
   
      PlayerProfile also has a method that loads the profiles.p file and returns all player names as a list.
    """
    
    def __init__(self):
          #PlayerProfile attributes
          #if you add an attribute, be sure to add it to the loadPlayerFile() method
        self.__playerName="???"
        self.__difficulty=0
        self.__highScore=0
        self.__bestStepRun=0
        self.__levelReached=1
        self.__songDictionary={}
        self.__filename = ""
        
    def __str__(self):
        return "%s. High score=%s. Best step run=%s. Highest level reached=%s. Difficulty=%s"%(self.__playerName, self.__highScore, self.__bestStepRun, self.__levelReached, self.__difficulty)
    
    def __setPlayerFilename(self):
        """
           Used internally to create a filename for the player based on login name.
        """
        if self.__playerName != "???":
            l=self.__playerName.rsplit(" ")
            nameWithoutSpaces="_".join(l)
            self.__filename = fileLocs.playerProfiles+"\\"+nameWithoutSpaces+r".p"

    def loadPlayerFile (self):
        """
           Pass in the player's already-registered account name, and loadPlayerFile
           will look for a matching player account.
        """
        #print self.__filename
        if self.__filename == "":
            self.__setPlayerFilename()
        #print "filename= " + self.__filename            
        try:
            #filename handled internally -- derive it from playerName
#            print self.__filename
            f = open(self.__filename, "r")
            tempIn = pickle.load(f)
            self.__playerName = tempIn.getPlayerName()
            self.setBestStepRun(tempIn.getBestStepRun())
            self.__songDictionary = tempIn.getAllSongs()
            self.setDifficulty(tempIn.getDifficulty())
            self.setHighScore(tempIn.getHighScore())
            self.setLevelReached(tempIn.getLevelReached())
            f.close()                       
        except IOError:
            raise PlayerIOError("Unable to read player info from file.")
        
    def savePlayerInfo(self):
        """
           Saves player info to file with filename based on player name         
        """
        if self.__filename == "":
            self.__setPlayerFilename()
        try:
            #f = open(self.__filename, "w")
            pickle.dump(self, open(self.__filename, "w"))
            return True
            #f.close()
        except IOError:
            raise PlayerIOError("Unable to write player info to file.")
    
    def setHighScore(self, score):
        """
           Sets current high score to score passed in only if new score is higher.
           Returns true if the change was successful, otherwise returns false
        """
        if (self.__highScore < score):
            self.__highScore = score
            return True
        else:
            return False
        
    def deleteThisPlayerProfile(self):
        """
           This will delete the player from the profiles list and delete
           player's .p file.  The player's name must have already been set.
           Returns true on success.
        """
        #delete player from profiles.p
        filename = fileLocs.playerProfiles+r"\profiles.p"
        playerList = []
        if self.__filename == "":
            self.__setPlayerFilename()
        f = None
        result = False
        try:
            f = open(filename, "r")
            playerList = pickle.load(f)
            f.close()
            try:
                playerList.remove(self.getPlayerName())
                f = open(filename, "w")
                pickle.dump(playerList, f)
                f.close()
                os.remove(self.getPlayerFilename())
                return True ## name found and removed -- return true
            except ValueError:
                return False #unsuccessful delete -- return false 
            except IOError:
                return False
            except WindowsError:
                return False #file not found returned if player profile has never been saved to file     
        except IOError:
            return False # no file found -- return false
        
        
    def setExistingPlayerName(self, playerName):
        """
           Used to both check that a player account has already been created
           and update the current PlayerProfile with that account name. Returns
           true on success, false on failure.
        """
        if self.__playerAlreadyExists(playerName):
            self.__playerName = playerName
            return True
        else:
            return False
    
    
    def setNewPlayerName(self, playerName):
        """
           Sets player name to passed-in name only if no name has already been set.
           If the passed-in playerName is already in use, the name will not be
           added to the list a second time.  The method returns true if the
           name is added, otherwise it will return false.
        """
        if(self.__playerName=="???" and not(self.__playerAlreadyExists(playerName)) ):
              #verify that there isn't already a player by this name
            fileLocs=FileLocations()
            filename = fileLocs.playerProfiles+r"\profiles.p"
            playerList = []
            index = -1
            f = None
            try:
                  #load list of players -- if there's no file, then we skip this step 
                f = open(filename, "r")
                playerList = pickle.load(f)
                f.close()                
            except IOError:    
                pass
            finally:
                  #add name to list
                self.__playerName=playerName
                playerList.append(playerName)
                try:
                    f = open(filename,"w")
                    pickle.dump(playerList, f)
                    f.close()
                    self.savePlayerInfo()
                except IOError:
                    raise PlayerIOError("Unable to add player name to profile.p")
                return True
        else:
            return False ##unsuccessful -- return false

                
    def __playerAlreadyExists(self, playerName):
        """
            Checks profiles.p to see if the name is already on the list.
            Returns true if the name is on the list, otherwise returns false.
        """
        fileLocs = FileLocations()
        filename = fileLocs.playerProfiles+r"\profiles.p"
        playerList = []
        f = None
        try:
            f = open(filename, "r")
            playerList = pickle.load(f)
            f.close()
            try:
                index = playerList.index(playerName)
                return True ## name found as key -- return true
            except ValueError:
                return False #key not found -- return false      
        except IOError:
            return False # no file found -- return false

    def setDifficulty(self, difficulty):
        """
           Sets current difficulty using numeric values 0-2
           Returns true if the change was successful, otherwise
           returns false
        """
        if(0<= difficulty and difficulty <=2):
            self.__difficulty=difficulty
            return True
        else:
            return False
        
    def setBestStepRun(self, stepRun):
        """
           Sets player's best step run to passed in value only
           if new value is higher.  Returns true if the change 
           was successful, otherwise returns false
        """
        if(self.__bestStepRun < stepRun):
            self.__bestStepRun = stepRun
            return True
        else:
            return False
    
    def setLevelReached(self, level):
        """
           Sets player's highest level to passed-in value only if 
           new value is higher and if the new value is in the range
           1-5.  Returns true if the change was successful,
           otherwise returns false.
        """
        
        if(0 < level and level < 6 and self.__levelReached < level):
            self.__levelReached = level
            self.savePlayerInfo()
            return True
        else:
            return False
        print"level reached: "  + self.__levelReached
        
        
        
    def addSong(self, title, filename):
        """
           Adds passed-in song to player's song dictionary.  Song title and filename
           should both be Strings.  Returns true if add was successful--otherwise, it
           returns false.  The filename should actually be the complete path to the song
           on the user's system.
        """
        #make sure that the filename is valid? or does this happen outside?
        self.__songDictionary[title]=filename
        return True
        
    def getHighScore(self):
        return self.__highScore
    
    def getPlayerName(self):
        return self.__playerName
    
    def getDifficulty(self):
        return self.__difficulty
    
    def getBestStepRun(self):
        return self.__bestStepRun
    
    def getLevelReached(self):
        return self.__levelReached
    
    def getSongFilename(self, title):
        """
           Returns the filename of the song title given.  
           Will return empty string if title isn't in list or if it is misspelled.
        """
        try:
            f = self.__songDictionary[title]
        except KeyError:
            f = ""
        return f
    
    def getAllSongs(self):
        """
           Returns all songs in the player's playlist.
        """
        return self.__songDictionary
    
    def getPlayerFilename(self):
        """
           Returns the filename where player data is stored.  If no player is set,
           returns empty string.
        """
        if (self.__playerName != "???"):
            return self.__filename
        else:
            return ""
        
    def dispose(self):
        """
           Sets all values to default.
        """
        self.__playerName="???"
        self.__difficulty=0
        self.__highScore=0
        self.__bestStepRun=0
        self.__levelReached=1
        self.__songDictionary={}  
        self.__filename = ""  
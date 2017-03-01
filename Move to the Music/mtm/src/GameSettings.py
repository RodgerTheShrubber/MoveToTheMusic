"""
   GameSettings saves certain game settings across sessions.
   On first use, it will create a save file with default settings which
   the player then can edit in other menus.  On subsequent loads,
   GameSettings will then load the previously saved data.
"""

"""
   Started 29 March 2008 by Jason Cisarano.  30 March -- added persistence across sessions
"""

import cPickle as pickle
import os
from FileLocations import FileLocations

class GameSettingsIOError(Exception):
    """
       Custom error message for problems with loading and saving files
    """
    def __init__(self, message):
        self.__message = message
    def __str__(self):
        return repr(self.__message)

class GameSettings (object):
    """
       GameSettings saves certain game settings across sessions.
       On first use, it will create a save file with default settings which
       the player then can edit in other menus.  On subsequent loads,
       GameSettings will then load the previously saved data.
    """    
    def __init__(self):
        if not self.__loadGameSettings():
            self.__createNewGameSettings()
            
    def __loadGameSettings(self):
        try:
            #filename handled internally -- derive it from playerName
            fileLocs=FileLocations()
            filename = fileLocs.playerProfiles+r"\gameProfile.p"
            print '----------',filename
            f = open(filename, "r")
            tempIn = pickle.load(f)
            
            mVol = tempIn.getMusicVolume()
            vVol = tempIn.getVoiceVolume()
            fxVol = tempIn.getFxVolume()
            self.setVolumes(mVol, vVol, fxVol)
            width, height = tempIn.getScreenSize()
            self.setScreenSize(width, height)
            f.close()
            return True                       
        except IOError:
            return False
        except:
            print '123'
            return False
        
    def __saveGameSettings(self):
        """
           Saves this Settings to /Settingss/gameSettings.p
           Only one Settings is saved on a given machine. 
        """
        fileLocs=FileLocations()
        filename = fileLocs.playerProfiles+r"\gameProfile.p"
        print 'this is the filename ',filename
        try:
            f = open( filename, "w")
            pickle.dump(self, f)
            return True
        except IOError:
            raise GameSettingsIOError("Unable to write game Settings to file.")
    
    def __createNewGameSettings(self):
        self.setVolumes()
        self.setScreenSize()
        self.__saveGameSettings()

    def getScreenSize(self):
        """
           Return current screen size as tuple
        """
        return (self.__screen_x, self.__screen_y)
    
    def getVolumes(self):
        """
           Return all three volumes as tuple in this order:
           (musicVol, voiceVol, fxVol)
        """
        return (self.getMusicVolume(), self.getVoiceVolume(), self.getFxVolume())
    
    def getMusicVolume(self):
        return self.__musicVolume
    
    def getVoiceVolume(self):
        return self.__voiceVolume
    
    def getFxVolume(self):
        return self.__fxVolume
    
    def setScreenSize(self, x=800, y=600):
        """
           Set screen size as one of three possibilities:
               (800, 600) (1024, 768) (1280,960)
           Default value is (800, 600)
        """
        if x != 800 and x != 1024 and x != 1280:
            return False
        elif y != 600 and y != 768 and y != 960:
            return False
        else:
            self.__screen_x = x
            self.__screen_y = y
            self.__saveGameSettings()
            return True
    
    def setVolumes(self, mVol=50, vVol=50, fxVol=50):
        """
           Set all three volumes at the same time.
           Default value of 50 set for any item not passed in.
        """
        if self.setMusicVolume(mVol):
            if self.setVoiceVolume(vVol):
                if self.setFxVolume(fxVol):
                    self.__saveGameSettings()
                    return True
        else:
            return False
    
    def setMusicVolume(self, mVol):
        """
           Volume as int 0 <= vol <= 100
        """
        if 0 <= mVol and mVol <= 100:
            self.__musicVolume = mVol
            self.__saveGameSettings()
            return True
        else:
            return False
            
    def setFxVolume(self, fxVol):
        """
           Volume as int 0 <= vol <= 100
        """
        if 0 <= fxVol and fxVol <= 100:
            self.__fxVolume = fxVol
            self.__saveGameSettings()
            return True
        else:
            return False
            
    def setVoiceVolume(self, vVol):
        """
           Vol as int 0 <= vol <= 100
        """
        if 0 <= vVol and vVol <= 100:
            self.__voiceVolume = vVol
            self.__saveGameSettings()
            return True
        else:
            return False
    
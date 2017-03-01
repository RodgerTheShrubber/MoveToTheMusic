"""
   IntroMenu displays menu items needed at the beginning of the game.  The GameController
   should create one IntroMenu object (can Python do Singletons?) and then call the 
   IntroMenu method draw().  This will loop while player makes his/her choices.  It has
   built-in input controllers that need no outside initialization.
   
   When the player has chosen a game mode and number of players, IntroMenu will return a 
   GameInfo object with the player's choices.
"""

"""
   Created 17 February by Jason Cisarano.  Created basic navigation and screen drawing functions.
   25 February -- modified to use internal loop as discussed in 15 Feb meeting.  Added scrolling and selection. JC
   10 March -- added graphical interface prototype, removed text items. JC
   12 March -- added audio interface prototype. JC
   24 March -- added support for return values for SinglePlayerMenu JC
   26 March -- added audio status method, improved handling of return values from sub menus JC
   29 March -- added support for changing screen size JC
   5 April -- added variable wait based on framerate tracking
"""

"""
   Navigation scheme is the same regardless of input method (keyboard, number pad, dance mat):
   ======================
   |  XX  | XX   |  XX   |
   ======================
   |  XX  | UP   |  XX   |
   ======================
   | BACK | XX   | ENTER |
   ======================
   |  XX  | DOWN |  XX   |
   ======================
"""
import sys
sys.path.append(r"C:\Users\Public\MTM\mtm\songs")
import pygame
from pygame.locals import *
from GoodStep import GoodStep
from Controller import Controller
from GameInfo import GameInfo
from LoginMenu import LoginMenu
from SinglePlayerMenu import SinglePlayerMenu
from SetupMenu import SetupMenu
from EndCreditsScreen import EndCreditsScreen
from FileLocations import FileLocations
import SinglePlayerMode
    
class ScreenInfo():
    """
       Holds standard info about display including font and font size.
    """
    pygame.init()
    game = GameInfo()
    SCREEN_SIZE = game.getSettings().getScreenSize()
    font = pygame.font.SysFont("arial", 16);
    font_height = font.get_linesize()
    
class IntroMenu (object):
    """
       IntroMenu displays menu items needed at the beginning of the game.  The GameController
       should create one IntroMenu object (can Python do Singletons?) and then call the 
       IntroMenu method draw().  This will loop while player makes his/her choices.  It has
       built-in input controllers that need no outside initialization.
       
       When the player has chosen a game mode and number of players, IntroMenu will return a 
       GameInfo object with the player's choices.
    """
    def __init__(self, screen):
        """
           Set default values for font, menu items
        """
        self.__game = GameInfo()
        self.__cntrl = Controller()
        #self.__difficulty = self.__game.getPlayer(0).getProfile().getDifficulty()
        
        self.__screen = screen
        self.__screen_size = screen.get_size()
        self.__loadImages()
             
        self.__selected = 0
        self.__font = pygame.font.SysFont("arial", 48)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
          #initialize menus and set starting menu to main
        self.__initMenus()
        self.__loadAudio()
        
        self.__timeOld = pygame.time.get_ticks()

    def __initMenus(self):
        """
           Initialize all menus needed for IntroMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems and currentMenuColors attributes.
        """
        self.__menuItems=["Login", "Play", "Setup", "Quit"]
        #self.__menuItems=["Login", "Play", "Single Player", "Multiplayer", "Setup", "Quit"]
        
    def __checkNavEvent(self, step):
        """
           Looks at GoodStep item, updates self.selected as appropriate.
        """
        "Scroll down logic -- down arrow"
        if(step.getLocation()==(1, 0)):
              #update selected
            self.__selected += 1
            if self.__menuItems.__len__()-1 < self.__selected:
                self.__selected = 0
            self.__playSound(self.__menuSound[self.__selected])
            
        "Scroll up logic -- up arrow"
        if(step.getLocation()==(1, 2)):
              #update selected
            self.__selected -= 1
            if self.__selected < 0:
                self.__selected = self.__menuItems.__len__()-1
            self.__playSound(self.__menuSound[self.__selected])
        
        "Choose an option logic -- right arrow"
        if(step.getLocation()==(2, 1)):
            if self.__menuItems[self.__selected] == "Quit":
                #self.__game.__pp.savePlayerInfo()
                endCredits = EndCreditsScreen( self.__screen )
                endCredits.drawEndCredits()
                exit()
            
            if self.__menuItems[self.__selected] == "Login":
                loginMenu = LoginMenu(self.__screen, self.__game)
                self.__game.getPlayer(0).setProfile( loginMenu.drawLoginMenu())
                loginMenu = None
                return True
            
            if self.__menuItems[self.__selected] == "Setup":
                setupMenu = SetupMenu(self.__screen, self.__game)
                music, voice, fx, screensize = setupMenu.drawSetupMenu()
                self.__game.getSettings().setMusicVolume(music)
                self.__game.getSettings().setVoiceVolume(voice)
                self.__game.getSettings().setFxVolume(fx)
                if self.__screen_size != screensize:
                    width, height = screensize
                    self.__game.getSettings().setScreenSize(width, height)
                    self.__screen_size = self.__game.getSettings().getScreenSize()
                    self.__loadImages()
                    screen = pygame.display.set_mode((width,height), FULLSCREEN, 32)
                setupMenu = None
                return True
            
#            if self.__menuItems[self.__selected] == "Single Player":
#                singlePlayerMenu = SinglePlayerMenu(self.__screen, self.__game)
#                mode, numPlayers, difficulty = singlePlayerMenu.drawSPMenu()
#                self.__game.setGameMode(mode)
#                self.__game.setDifficulty(difficulty)
#                self.__game.setNumPlayers(numPlayers) # this is temporary?
#                singlePlayerMenu = None
#                return True
            
            #if self.__menuItems[self.__selected] == "Multiplayer":
                #self.__game.setNumPlayers(2)
                #self.__narrationChannel.play(self.__buzzer)
                #return True
            
            if self.__menuItems[self.__selected] == "Play":
                singlePlayerMenu = SinglePlayerMenu(self.__screen, self.__game)
                mode, difficulty = singlePlayerMenu.drawSPMenu()
                self.__game.setGameMode(mode)
                #self.__difficulty = difficulty
                self.__game.getPlayer(0).getProfile().setDifficulty(difficulty)
                singlePlayerMenu = None
                return True

        
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
        menuImage_file = fileLocs.images_menus+r"\mainmenu_a.png"
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        
        self.__menuImage = pygame.image.load(menuImage_file).convert_alpha()
        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()
        
          #settings for placement on screen  -- default items
        self.__offset_x = 80
        self.__offset_y = 50
        self.__menuItem_height = 105
        self.__menu_Y_bump = 10 #centers the note on menu item
          
        screen_x, screen_y = self.__screen_size
        
          #adjust image dimensions according to screen size if needed
        if(screen_x != 1280):
            transform = 0
            if(screen_x == 800):
                transform = 0.625
            elif(screen_x == 1024):
                transform = 0.8
            self.__offset_x = self.__offset_x * transform 
            menu_x, menu_y = self.__menuImage.get_size()
            menu_x = int(menu_x * transform)
            menu_y = int(menu_y * transform)
            note_x, note_y = self.__noteImage.get_size()
            note_x = int(note_x * transform)
            note_y = int(note_y * transform)
            self.__menuImage = pygame.transform.scale( self.__menuImage, (menu_x, menu_y))
            self.__noteImage = pygame.transform.scale( self.__noteImage, (note_x, note_y))
            self.__menuItem_height = int(self.__menuItem_height * transform)
            
        self.__bkgrd_x = screen_x - self.__bkgrd_rightImage.get_width()
        self.__bkgrd_y = screen_y - self.__bkgrd_rightImage.get_height()
        
        
    def __loadAudio(self):
        """
            Loads voice and sound effects files for this menu.
        """
        fileLocs=FileLocations()
        self.__menuSoundsFilename=["\menu_01_01.ogg", "\menu_01_02.ogg", "\menu_01_05.ogg","\menu_01_06.ogg"]
        #self.__menuSoundsFilename=["\menu_01_01.ogg", "\menu_01_02.ogg", "\menu_01_03.ogg", "\menu_01_04.ogg", "\menu_01_05.ogg", "\menu_01_06.ogg"]
        self.__menuSound=[]
        for filename in self.__menuSoundsFilename:
            self.__menuSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
            
        self.__buzzer = pygame.mixer.Sound(fileLocs.soundEffects+"\\fx_00_00.ogg")
        self.__narrationChannel = pygame.mixer.Channel(0)

    def __playSound(self, soundFile):
        """
           Plays soundFile on __narrationChannel.  Only one sound can be played at a time
           and subsequent sounds will override one another.
        """
        soundValue = self.__game.getSettings().getVoiceVolume() / 100.0
        soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)
        
    def __initMenuStatus(self):
        """
           Builds a list of files that describe the player's current game choices and login settings.
           Must be used before __playMenuStatus
        """
        fileLocs=FileLocations()
        self.__statusIndex = 0
        self.__statusPlaying = True
        
          #build the list of files to play
        self.__status =[pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_04.ogg")]
        if self.__game.getNumPlayers() == 1:
            self.__status.append(pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_05.ogg"))
        else:
            self.__status.append(pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_06.ogg"))
        if self.__game.getGameMode() == 0:
            self.__status.append(pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_07.ogg"))
        else:
            self.__status.append(pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_08.ogg"))
        if self.__game.getPlayer(0).getName()=="New player":
            self.__status.append(pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_02.ogg"))
        else:
            self.__status.append(pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_00_03.ogg"))
        
    def __playMenuStatus(self):
        """
           Plays only one file at a time to allow for player input
           __initMenuStatus must be called before this method to create sound list
           or update it to latest player choices.
        """
        if self.__statusPlaying and not self.__narrationChannel.get_busy():
            self.__narrationChannel.play(self.__status[self.__statusIndex])
            self.__statusIndex += 1
            if self.__statusIndex == self.__status.__len__():        
                self.__statusPlaying = False

    def __sleep(self):
        """
           Calculates wait time based on target framerate of 30 fps.  Returns wait time in milliseconds.
        """
        target_wait_in_millis = 33
        timeDiff = pygame.time.get_ticks() - self.__timeOld
        wait = target_wait_in_millis - timeDiff
        if wait < 5:
            wait = 5
        
        pygame.time.wait(wait)
        self.__timeOld = pygame.time.get_ticks()

    def drawIntroMenu(self, screen):
        """
           Draws menu to screen.  Takes control of game while menus are displayed.
           Menu can change based on menu level (some items have sub-levels) and 
           what item is selected.  Currently selected item is highlighted.
           Parameter is screen currently in use.
        """
        notDone=True
        firstTime=True
        
        self.__initMenuStatus()

        while notDone:
            self.__screen.fill((74, 83, 71))
            event = pygame.event.poll() ##having poll uses lots of cpu -- but it allows for __playMenuStatus   
            if not(self.__cntrl.checkEvent(event) == None):
                self.__statusPlaying = False
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            yChange = 0
            
            screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
            screen.blit(self.__menuImage, (self.__offset_x, self.__offset_y))
            screen.blit(self.__noteImage, (self.__offset_x/8, self.__offset_y + (self.__selected * self.__menuItem_height) + self.__menu_Y_bump))
            screen.blit(self.__font.render(str(self.__game.getPlayer(0).getName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
                        
            pygame.display.flip()
            self.__sleep() # gives 30 fps max, limits cpu use

        return self.getGameInfo()

    def getGameInfo(self):
        """
           Returns game info as determined by user input.
        """
        return self.__game
         
"""
   SinglePlayerMenu displays menu items specific to single player game.  The object
   should be created by IntroMenu only if the player selects the single player options.
   Like IntroMenu, the draw() method has a built-in loop that controls the view while
   the player makes his/her choices.  It has
   built-in input controllers that need no outside initialization.
   
   IntroMenu should pass in the current GameInfo object as a parameter and 
   SinglePlayerMenu will return a tuple when complete:
   (gameMode (as string), numPlayers, difficulty)
"""

"""
   Created 21 March by Jason Cisarano, based on code from IntroMenu.  24 March -- added difficulty settings.
   26 March -- Completed difficulty, added game mode picker.
"""

"""
   Navigation scheme is the same for all menus regardless of input method (keyboard, number pad, dance mat):
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

import pygame
from pygame.locals import *
from GoodStep import GoodStep
from Controller import Controller
from GameInfo import GameInfo
from LoginMenu import LoginMenu
from FileLocations import FileLocations
from SongChooserMenu import SongChooserMenu
from MyMusicMenu import MyMusicMenu

class SinglePlayerMenu (object):
    """
       SinglePlayerMenu displays menu items specific to single player game.  The object
       should be created by IntroMenu only if the player selects the single player options.
       Like IntroMenu, the draw() method has a built-in loop that controls the view while
       the player makes his/her choices.  It has
       built-in input controllers that need no outside initialization.
       
       IntroMenu should pass in the current GameInfo object as a parameter and 
       SinglePlayerMenu will return a tuple when complete:
       (gameMode (as string), numPlayers, difficulty)
    """
    
    def __init__(self, screen, gameInfo):
        """
           Set default values for font, menu items
        """
        self.__game = gameInfo
        self.__game.setNumPlayers(1)
        self.__cntrl = Controller()
        
        self.__selected = 0
        self.__diffSelected = self.__game.getPlayer(0).getProfile().getDifficulty()
        self.__modeSelected = self.__game.getGameModeAsInt()
        self.__font = pygame.font.SysFont("arial", 48)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
          #visual elements
        self.__screen = screen
        self.__screen_size = screen.get_size()
        self.__loadImages()
        
          #initialize menus and set starting menu to main
        self.__initMenus()
        self.__loadAudio()

    def __initMenus(self):
        """
           Initialize all menus needed for SinglePlayerMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems.
        """
        self.__menuItems=["Change mode", "Change difficulty", "Play","My Music", "Done"]
        
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
            if self.__menuItems[self.__selected] == "Done":
                return False #false breaks out of loop, allows return to prev menu
            
            if self.__menuItems[self.__selected] == "Play":
                songMenu = SongChooserMenu(self.__screen, self.__game)            
                songMenu.drawSongChooserMenu(self.__screen)
                return True
            if self.__menuItems[self.__selected] == "My Music":
                songMenu = MyMusicMenu(self.__screen, self.__game)            
                songMenu.drawSongChooserMenu(self.__screen)
                return True

            if self.__menuItems[self.__selected] == "Change mode":
                  #must be logged in to play challenge mode
                if self.__game.getPlayer(0).getName() == "New player":
                    self.__playSound(self.__modeChange_fail)
                    return True
                
                  #toggle modes if logged in
                self.__modeSelected += 1
                if self.__modeImage.__len__()-1 < self.__modeSelected:
                    self.__modeSelected = 0
                self.__playSound(self.__modeSound[self.__modeSelected])
                self.__placeModeImg()
                self.__game.setGameMode(self.__modeSelected)
                return True 

            if self.__menuItems[self.__selected] == "Change difficulty":
                self.__diffSelected += 1
                if self.__difficultyImage.__len__()-1 < self.__diffSelected:
                    self.__diffSelected = 0
                self.__playSound(self.__difficultySound[self.__diffSelected])
                self.__placeDiffImg()
                self.__game.getPlayer(0).getProfile().setDifficulty(self.__diffSelected)
                return True
            
        "Escape -- left arrow"
        if(step.getLocation()==(0,1)):
            return False
        
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
        menuImage_file = fileLocs.images_menus+r"\playermenu_b.png"
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        
        self.__menuImage = pygame.image.load(menuImage_file).convert_alpha()
        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()        
        
          #mode inserts
        self.__modeImage_file=["\\free.png","\challenge.png"]
        self.__modeImage=[]
        for filename in self.__modeImage_file:
            self.__modeImage.append(pygame.image.load(fileLocs.images_menus+filename).convert_alpha())
          
          #difficulty inserts
        self.__difficultyImage_file=["\easy_a.png", "\\tough.png", "\cruel.png"]
        self.__difficultyImage=[]
        for filename in self.__difficultyImage_file:
            self.__difficultyImage.append(pygame.image.load(fileLocs.images_menus+filename).convert_alpha())
        
          #settings for placement on screen  -- default items
        self.__offset_x = 80
        self.__offset_y = 50
        self.__menuItem_height = 125
        self.__menu_Y_bump = 10 #centers the note on menu item
          
        screen_width, screen_height = self.__screen_size
          #adjust dimensions according to screen size if needed
        if(screen_width != 1280):
            transform = 0
            if(screen_width == 800):
                transform = 0.625
            elif(screen_width == 1024):
                transform = 0.8
            self.__offset_x = self.__offset_x * transform 
            
            menu_x, menu_y = self.__menuImage.get_size()
            menu_x = int(menu_x * transform)
            menu_y = int(menu_y * transform)
            note_x, note_y = self.__noteImage.get_size()
            note_x = int(note_x * transform)
            note_y = int(note_y * transform)
            
            for image in self.__difficultyImage:
                x, y = image.get_size()
                x = int(x * transform)
                y = int(y * transform)
                #image = pygame.transform.scale(image, (x,y))
                self.__difficultyImage[self.__difficultyImage.index(image)] = pygame.transform.scale(image, (x, y))
                
            for image in self.__modeImage:
                x,y = image.get_size()
                x = int(x * transform)
                y = int(y * transform)
                self.__modeImage[self.__modeImage.index(image)] = pygame.transform.scale(image, (x,y))
                
            self.__menuImage = pygame.transform.scale(self.__menuImage, (menu_x, menu_y))
            self.__noteImage = pygame.transform.scale(self.__noteImage, (note_x, note_y))
            self.__menuItem_height = int(self.__menuItem_height * transform)
        
          #determine placement for the difficulty inset
        self.__placeDiffImg()
        self.__placeModeImg()
        self.__bkgrd_x = screen_width - self.__bkgrd_rightImage.get_width()
        self.__bkgrd_y = screen_height - self.__bkgrd_rightImage.get_height()
    
    def __placeDiffImg(self):
        """
           set placement of difficulty inset based on current screen size
        """
        x,y = self.__difficultyImage[self.__diffSelected].get_size()
        screen_w, screen_h = self.__screen_size
        self.__diff_x = screen_w/2 + x/4 
        self.__diff_y = int(self.__offset_y + self.__menuItem_height)
        
    def __placeModeImg(self):
        """
           set placement of mode inset based on current screen size
        """
        x,y = self.__modeImage[self.__modeSelected].get_size()
        screen_w, screen_h = self.__screen_size
        self.__mode_x = screen_w/2 - x/4  
        self.__mode_y = int( self.__offset_y )
        
        
    def __loadAudio(self):
        """
            Loads voice and sound effects files for this menu.
        """
        fileLocs=FileLocations()
        self.__menuSoundFilename=["\menu_03_01.ogg", "\menu_03_03.ogg", "\menu_01_02.ogg","\menu_01_07.ogg", "\menu_00_01.ogg"]
        self.__menuSound=[]
        for filename in self.__menuSoundFilename:
            self.__menuSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
            
          #difficulty insert sounds
        self.__difficultySoundFilename=["\menu_00_10.ogg", "\menu_00_11.ogg", "\menu_00_12.ogg"]
        self.__difficultySound=[]
        for filename in self.__difficultySoundFilename:
            self.__difficultySound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
            
          #mode insert sounds
        self.__modeSoundFilename=["\menu_00_07.ogg","\menu_00_08.ogg"]
        self.__modeSound=[]
        for filename in self.__modeSoundFilename:
            self.__modeSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
        
          #one-off sounds
        self.__modeChange_fail = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_03_04.ogg")
                
          #use one channel for narration to avoid multiple voice items playing at the same time
        self.__narrationChannel = pygame.mixer.Channel(0)

    def __playMenuItemSound(self, selected):
        self.__narrationChannel.play(self.__menuSound[selected])
        pass
    
    def __playDiffSound(self, diffSelected):
        self.__narrationChannel.play(self.__difficultySound[diffSelected])
        
    def __playModeSound(self, modeSelected):
        self.__narrationChannel.play(self.__modeSound[modeSelected])
        
    def __playSound(self, soundFile):
        soundValue = self.__game.getSettings().getVoiceVolume() / 100.0
        soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)        
       
    def drawSPMenu(self):
        """
           Draws menu to screen.  Takes control of game while menus are displayed.
           Menu can change based on menu level (some items have sub-levels) and 
           what item is selected.  Currently selected item is highlighted.
        """
        notDone=True
        
          #play first item on first load
        self.__playSound(self.__menuSound[self.__selected])
        
        while notDone:
            self.__screen.fill((74, 83, 71))
            event = pygame.event.wait()        
            if not(self.__cntrl.checkEvent(event) == None):
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            yChange = 0
            
            self.__screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
            self.__screen.blit(self.__menuImage, (self.__offset_x, self.__offset_y))
            self.__screen.blit(self.__noteImage, (self.__offset_x/8, self.__offset_y + (self.__selected * self.__menuItem_height) + self.__menu_Y_bump))
            self.__screen.blit(self.__difficultyImage[self.__diffSelected], (self.__diff_x, self.__diff_y))
            self.__screen.blit(self.__modeImage[self.__modeSelected], (self.__mode_x, self.__mode_y))
            self.__screen.blit(self.__font.render(str(self.__game.getPlayer(0).getName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
                        
            pygame.display.flip()
            pygame.time.wait(2)
        
        self.__screen.fill((74, 83, 71))
        return self.getSPInfo()

    def getSPInfo(self):
        """
           Returns tuple: (gameMode, difficulty)
        """
        return (self.__game.getGameMode(), self.__game.getPlayer(0).getProfile().getDifficulty())
         
"""
   SetupMenu displays volume and screen size options.  It should get a GameInfo object
   from IntroMenu, and then it will return the changed settings as a tuple:
   (musicVolume, voiceVolume, fxVolume, (screenSizeX, screenSizeY))
   The object should be created by IntroMenu only if the player selects the single player options.
   Like IntroMenu, the draw() method has a built-in loop that controls the view while
   the player makes his/her choices.  It has built-in input controllers that need no outside initialization.
"""

"""
   Created 26 March by Jason Cisarano, based on code from SinglePlayerMenu.  27 March added volume controls and screen size visual JC.
   29 March made voicevolume control work within navigation and made screensize active JC
   10 April -- now only hardware-supported screen sizes are displayed, added play first choice on initial load
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
    

class SetupMenu (object):
    """
       SetupMenu displays volume and screen size options.  It should get a GameInfo object
       from IntroMenu, and then it will return the changed settings as a tuple:
       (musicVolume, voiceVolume, fxVolume, (screenSizeX, screenSizeY))
       The object should be created by IntroMenu only if the player selects the single player options.
       Like IntroMenu, the draw() method has a built-in loop that controls the view while
       the player makes his/her choices.  It has built-in input controllers that need no outside initialization.
    """
    
    def __init__(self, screen, gameInfo):
        """
           Set default values for font, menu items
        """
        self.__game = gameInfo
        
        ##### i added this code 
        self.__settings = self.__game.getSettings()
        ####
        
        self.__cntrl = Controller()
        
        self.__screen = screen
        self.__screen_size = screen.get_size()
        
        self.__selected = 0
        self.__screensize_selected = 0
        self.__volumeIncrement = 10
        
        self.__font = pygame.font.SysFont("arial", 48)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
          #initialize menus and set starting menu to main
        self.__initMenus()
        self.__loadAudio()
        self.__loadImages()


    def __initMenus(self):
        """
           Initialize all menus needed for SinglePlayerMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems.
        """
        self.__menuItems=["Music volume", "Voice volume", "Sound fx volume", "Screen size", "Done"]
        self.__screensizeImage_file = []
        self.__screenSizes = []
        __potentialScreenSizes={(800,600):"\\800x600.png", (1024,768):"\\1024x768.png", (1280,960):"\\1280x960.png"}
        for key, filename in __potentialScreenSizes.iteritems():
            if key in pygame.display.list_modes():
                self.__screenSizes.append(key)
             
             
        #add in 1280 so i can use it
        #the hack breaks my game-- i get an index out of bounds error when I change screen size -- jc
        self.__screenSizes.append((1280,960))   
          #add filenames to list in order
        self.__screenSizes.sort()
        for key in self.__screenSizes:
            self.__screensizeImage_file.append(__potentialScreenSizes[key])
            
          #set screensize display to current screensize
        self.__screensize_selected = self.__screenSizes.index(self.__screen_size)

        
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
            
            if self.__menuItems[self.__selected] == "Screen size":
                self.__screensize_selected += 1
                if self.__screensizeImage.__len__()-1 < self.__screensize_selected:
                    self.__screensize_selected = 0
                self.__playSound(self.__screensizeSound[self.__screensize_selected])
                width,height = self.__screenSizes[self.__screensize_selected]
                self.__settings.setScreenSize(width,height)
                self.__screen_size = self.__settings.getScreenSize()
                self.__loadImages()
                screen = pygame.display.set_mode((width,height), FULLSCREEN, 32)
                #self.__placeScreensizeImg()

            if self.__menuItems[self.__selected] == "Music volume":
                  #raise music volume
                self.__settings.setMusicVolume(self.__settings.getMusicVolume() + self.__volumeIncrement)
                self.__playSound(self.__louderSound)
                return True 

            if self.__menuItems[self.__selected] == "Voice volume":
                  #raise voice volume
                self.__settings.setVoiceVolume(self.__settings.getVoiceVolume() + self.__volumeIncrement)
                self.__playSound(self.__louderSound)
                return True
            
            if self.__menuItems[self.__selected] == "Sound fx volume":
                  #raise fx volume
                self.__settings.setFxVolume(self.__settings.getFxVolume() + self.__volumeIncrement)
                self.__playSound(self.__louderSound)
                return True
            
        "Choose an option logic -- right arrow -- in this menu only, right arrow used to lower volumes"
        if(step.getLocation()==(0, 1)):
            if self.__menuItems[self.__selected] == "Music volume":
                  #lower music volume
                self.__settings.setMusicVolume(self.__settings.getMusicVolume() - self.__volumeIncrement)
                self.__playSound(self.__quieterSound)
                return True 

            if self.__menuItems[self.__selected] == "Voice volume":
                  #lower voice volume
                self.__settings.setVoiceVolume(self.__settings.getVoiceVolume() - self.__volumeIncrement)
                self.__playSound(self.__quieterSound)
                return True
            
            if self.__menuItems[self.__selected] == "Sound fx volume":
                  #lower fx volume
                self.__settings.setFxVolume(self.__settings.getFxVolume() - self.__volumeIncrement)
                self.__playSound(self.__quieterSound)
                return True
            
#            if self.__menuItems[self.__selected] == "Done":
#                "Hitting left arrow on the Done item allows quit without setting values"
#                return False
        
        return True

  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
        menuImage_file = fileLocs.images_menus+r"\setupmenu.png"
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        
        self.__menuImage = pygame.image.load(menuImage_file).convert_alpha()
        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()

          #screensize inserts
        self.__screensizeImage=[]
        for filename in self.__screensizeImage_file:
            self.__screensizeImage.append(pygame.image.load(fileLocs.images_menus+filename).convert_alpha())

          #settings for placement on screen  -- default items
        self.__offset_x = 80
        self.__offset_y = 50
        self.__menuItem_height = 125
        self.__menu_Y_bump = 10 #centers the note on menu item
        
        self.__vol_num_x = 960
          
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
              
            for image in self.__screensizeImage:
                x, y = image.get_size()
                x = int(x * transform)
                y = int(y * transform)
                self.__screensizeImage[self.__screensizeImage.index(image)] = pygame.transform.scale(image, (x, y))
                
            self.__menuImage = pygame.transform.scale(self.__menuImage, (menu_x, menu_y))
            self.__noteImage = pygame.transform.scale(self.__noteImage, (note_x, note_y))
            self.__menuItem_height = int(self.__menuItem_height * transform)
            self.__vol_num_x = self.__vol_num_x * transform
        
          #determine placement for the screensize inset
        self.__placeScreensizeImg()
        self.__bkgrd_x = screen_width - self.__bkgrd_rightImage.get_width()
        self.__bkgrd_y = screen_height - self.__bkgrd_rightImage.get_height()

    
    def __placeScreensizeImg(self):
        """
           set placement of screensize inset based on width of image and current screen size
        """
        x, y = self.__screensizeImage[self.__screensize_selected].get_size()
        screen_w, screen_h = self.__screen_size
        self.__diff_x = int(screen_w/3*2 - x/2)   
        self.__diff_y = int(self.__offset_y + self.__menuItem_height * 3 + self.__menu_Y_bump)

        
    def __loadAudio(self):
        """
            Loads voice and sound effects files for this menu.
        """
        fileLocs=FileLocations()
        self.__menuSoundFilename=["\menu_04_02.ogg", "\menu_04_04.ogg", "\menu_04_06.ogg", "\menu_04_08.ogg", "\menu_00_01.ogg"]
        self.__menuSound=[]
        for filename in self.__menuSoundFilename:
            self.__menuSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
            
          #screensize insert sounds
        self.__screensizeSoundFilename=["\menu_04_11.ogg", "\menu_04_12.ogg", "\menu_04_13.ogg"]
        self.__screensizeSound=[]
        for filename in self.__screensizeSoundFilename:
            self.__screensizeSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
            
        self.__louderSound = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_04_10.ogg")
        self.__quieterSound = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_04_09.ogg")
                    
          #use one channel for narration to avoid multiple voice items playing at the same time
        self.__narrationChannel = pygame.mixer.Channel(0)


    def __playSound(self, soundFile):
        soundValue = self.__settings.getVoiceVolume() / 100.0
        soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)

       
    def drawSetupMenu(self):
        """
           Draws menu to screen.  Takes control of game while menus are displayed.
           Menu can change based on menu level (some items have sub-levels) and 
           what item is selected.  Currently selected item is highlighted.
        """
        notDone=True
        
          #play current choice when starting the menu
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
            self.__screen.blit(self.__font.render(str(self.__game.getPlayer(0).getName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
            self.__screen.blit(self.__font.render(str(self.__settings.getMusicVolume()), True, self.__font_color), (self.__vol_num_x, self.__offset_y))
            self.__screen.blit(self.__font.render(str(self.__settings.getVoiceVolume()), True, self.__font_color), (self.__vol_num_x, self.__offset_y + self.__menuItem_height))
            self.__screen.blit(self.__font.render(str(self.__settings.getFxVolume()), True, self.__font_color), (self.__vol_num_x, self.__offset_y + self.__menuItem_height * 2))            
            self.__screen.blit(self.__screensizeImage[self.__screensize_selected], (self.__diff_x, self.__diff_y))
            
            pygame.display.flip()
            pygame.time.wait(2)
        
        self.__screen.fill((74, 83, 71))
        return self.getSetupInfo()


    def getSetupInfo(self):
        """
           Returns tuple: (musicVolume, voiceVolume, fxVolume, screenSize)
        """
        return (self.__settings.getMusicVolume(), self.__settings.getVoiceVolume(), self.__settings.getFxVolume(), self.__screenSizes[self.__screensize_selected])
         
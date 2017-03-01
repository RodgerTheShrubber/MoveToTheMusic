"""
   IntroMenu gives the player a few training options for Move to the Music.  Like other menus,
   it presents a list of items that the player navigates with the dance mat.  When the player
   chooses an item, it either plays a short audio tutorial or moves to another screen that
   trains a specific task.  
"""

"""
   Created 17 April by Jason Cisarano
   22 April -- completed "How to play" tutorial
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

import pygame
from pygame.locals import *
#from utils.GoodStep import GoodStep
from Controller import Controller
from GameInfo import GameInfo
from SoundEffectController import SoundEffectController
from FileLocations import FileLocations
import ComboTutorial
    
class TutorialMenu (object):
    """
       IntroMenu gives the player a few training options for Move to the Music.  Like other menus,
       it presents a list of items that the player navigates with the dance mat.  When the player
       chooses an item, it either plays a short audio tutorial or moves to another screen that
       trains a specific task.  
    """
    
    def __init__(self, screen):
        """
           Set default values for font, menu items
        """
        self.__game = GameInfo()
        self.__cntrl = Controller()
        
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
        
        self.__menuStartTime = self.__timeOld = pygame.time.get_ticks()
        self.__framerateTimeOld = pygame.time.get_ticks()

    def __initMenus(self):
        """
           Initialize all menus needed for IntroMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems and currentMenuColors attributes.
        """
        self.__menuItems=["How to play", "Learn combos", "Done with instructions" ]
        
    def __checkNavEvent(self, step):
        """
           Looks at GoodStep item, updates self.selected as appropriate.
        """
        "Scroll down logic -- down arrow"
        if(step.getLocation()==(1, 0)):
            self.__soundController.flush()
              #update selected
            self.__selected += 1
            if self.__menuItems.__len__()-1 < self.__selected:
                self.__selected = 0
            self.__playSound(self.__menuSound[self.__selected])
            
        "Scroll up logic -- up arrow"
        if(step.getLocation()==(1, 2)):
            self.__soundController.flush()
              #update selected
            self.__selected -= 1
            if self.__selected < 0:
                self.__selected = self.__menuItems.__len__()-1
            self.__playSound(self.__menuSound[self.__selected])
        
        "Choose an option logic -- right arrow"
        if(step.getLocation()==(2, 1)):
            self.__soundController.flush()
            if self.__menuItems[self.__selected] == "Done with instructions":
                return False
            
            if self.__menuItems[self.__selected] == "Learn combos":
                ComboTutorial.startGame(self.__screen)
                return True
            
            if self.__menuItems[self.__selected] == "How to play":
                self.__soundController.flush()
                self.__soundController.queueSound( self.__howto1 )
                self.__soundController.queueSound( self.__howto2 )
                self.__soundController.queueSound( self.__howto3 )
                return True
            
        if(step.getLocation()==(0,1)):
            self.__soundController.flush()
            return False    
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
        menuImage_file = fileLocs.images_menus+r"\tutorialmenu.png"
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        
        self.__menuImage = pygame.image.load(menuImage_file).convert_alpha()
        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()
        
          #settings for placement on screen  -- default items
        self.__offset_x = 80
        self.__offset_y = 50
        self.__menuItem_height = 125
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
            self.__menuImage = pygame.transform.scale(self.__menuImage, (menu_x, menu_y))
            self.__noteImage = pygame.transform.scale(self.__noteImage, (note_x, note_y))
            self.__menuItem_height = int(self.__menuItem_height * transform)
            
        self.__bkgrd_x = screen_x - self.__bkgrd_rightImage.get_width()
        self.__bkgrd_y = screen_y - self.__bkgrd_rightImage.get_height()
        
        
    def __loadAudio(self):
        """
            Loads voice and sound effects files for this menu.
        """
        fileLocs=FileLocations()
        self.__menuSoundsFilename=["\menu_06_05.ogg", "\menu_06_06.ogg", "\menu_00_01.ogg" ]
        self.__menuSound=[]
        for filename in self.__menuSoundsFilename:
            self.__menuSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
            
        self.__welcomeMessage=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_06_01.ogg")
        self.__navMessage1=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_06_03.ogg")
        self.__navMessage2=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_06_04.ogg")
        
        self.__howto1=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_08_01.ogg")
        self.__howto2=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_08_02.ogg")
        self.__howto3=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_08_03.ogg")
        
        self.__soundController = SoundEffectController()
        self.__soundController.queueSound( self.__welcomeMessage )
        self.__soundController.queueSound( self.__navMessage1 )
        self.__soundController.queueSound( self.__navMessage2 )                
        
        self.__narrationChannel = pygame.mixer.Channel(0)

    def __playSound(self, soundFile):
        """
           Plays soundFile on __narrationChannel.  Only one sound can be played at a time
           and subsequent sounds will override one another.
        """
        soundValue = self.__game.getSettings().getVoiceVolume() / 100.0
        soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)
   
    def __sleep(self):
        """
           Calculates wait time based on target framerate of 30 fps.  Returns wait time in milliseconds.
        """
        target_wait_in_millis = 33
        timeDiff = pygame.time.get_ticks() - self.__framerateTimeOld
        wait = target_wait_in_millis - timeDiff
        if wait < 5:
            wait = 5
        
        pygame.time.wait(wait)
        self.__framerateTimeOld = pygame.time.get_ticks()
        
    def drawTutorialMenu(self, screen):
        """
           Draws menu to screen.  Takes control of game while menus are displayed.
           Menu can change based on menu level (some items have sub-levels) and 
           what item is selected.  Currently selected item is highlighted.
           Parameter is screen currently in use.
        """
        notDone=True
        firstTime=True
        self.__controllerUpdate = False

        while notDone:
            #print pygame.time.get_ticks() - self.__menuStartTime
            if self.__controllerUpdate == True or ( pygame.time.get_ticks() - self.__menuStartTime ) > 3000:
                self.__controllerUpdate = True
                self.__soundController.update()
            
            self.__screen.fill((74, 83, 71))
            event = pygame.event.poll()   
            if not(self.__cntrl.checkEvent(event) == None):
                self.__statusPlaying = False
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            yChange = 0
            
            screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
            screen.blit(self.__menuImage, (self.__offset_x, self.__offset_y))
            screen.blit(self.__noteImage, (self.__offset_x/8, self.__offset_y + (self.__selected * self.__menuItem_height) + self.__menu_Y_bump))
            screen.blit(self.__font.render(str(self.__game.getPlayer(0).getName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
                        
            pygame.display.flip()
            self.__sleep()

        return True
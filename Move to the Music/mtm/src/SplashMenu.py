"""
   SplashMenu displays the title/opening graphic and presents player with choice of
   playing tutorial or not.
"""

"""
   Begun 2 April by Jason Cisarano.
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

import pygame
import random
from pygame.locals import *
from GoodStep import GoodStep
from Controller import Controller
from FileLocations import FileLocations
from SoundEffectController import SoundEffectController
from Bouncer import Bouncer
from TutorialMenu import TutorialMenu
from bisect import bisect
from EndCreditsScreen import EndCreditsScreen

class SplashMenu (object):
    """
      SplashMenu displays the title/opening graphic and presents player with choice of
      playing tutorial or not.
    """
    
    def __init__(self, screen):
        """
           Set default values for font, menu items
        """
        self.__cntrl = Controller()
 
        self.__screen = screen
        self.__screen_size = screen.get_size()
        
           #initialize menus and set starting menu to main
        self.__initTitle()
        self.__loadAudio()
               
        self.__loadImages()
             
        self.__selected = 0
        self.__font = pygame.font.SysFont("arial", 48)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
          #init frame tracking stats
        self.__timeOld = pygame.time.get_ticks()
        self.__framerateTimeOld = pygame.time.get_ticks()
        self.__framerate = 0
        self.__framesCounted = 0

    def __initTitle(self):
        """
           Set title items and prepare for animation
        """
        self.__title = "MOVETothemusic"
        screenwidth, screenheight = self.__screen_size
        titlewidth = screenwidth - int(screenwidth * 0.2) ##add some buffer on either side of title
        letterspace = int(titlewidth/self.__title.__len__() +1)
        title_y = int(screenheight * 0.3) ##place in top third of screen
        self.__letterDictionary = {}
        for c in self.__title:
            #self.__letterDictionary[c] = Bouncer((int(screenwidth * 0.05) + (letterspace * self.__title.index(c))), title_y)
            self.__letterDictionary[c] = Bouncer((int(screenwidth * 0.1) + (letterspace * self.__title.index(c))), title_y)            

        self.__letterDictionary["m"].setBounce()
        
    def __updateTitle(self):
        """
           iterate over all title elements and update for current frame
        """
        if not self.__music.get_busy():
            return
        time_playing = self.__music.get_pos() * 0.001 ##get time since song start and convert from millis to seconds
        if self.__getDelta(time_playing) < 0.01:
            next_bouncer = random.randint(0, self.__letterDictionary.__len__() )
            if next_bouncer < self.__title.__len__():
                self.__letterDictionary[self.__title[next_bouncer]].setBounce()
 
    def __getDelta(self, t):
        """
            Calculate time difference to nearest beat
        """
        n = bisect(self.__times, t)
        d1 = t - self.__times[n-1]
        try:
            d2 = self.__times[n] - t
        except IndexError:
            return -d1
        if d1 < d2:
            return -d1
        else:
            return d2
            
    def __checkNavEvent(self, step):
        """
           Looks at GoodStep item, updates self.selected as appropriate.
        """
       
        "Choose an option logic -- right arrow"
        if(step.getLocation()==(2, 1)):
            #right arrow starts game
            self.__music.fadeout(4000)
            self.__soundController.flush()
            return False
            
        "Choose an option -- left arrow"
        if(step.getLocation()==(0,1)):
            self.__soundController.flush()
            tutorialMenu = TutorialMenu(self.__screen)
            self.__music.fadeout(4000)
            tutorialMenu.drawTutorialMenu(self.__screen)
            tutorialMenu = None
            return False
      
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()

          #background
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        button_file = fileLocs.images_menus+r"\splash_buttons.png"
        
          #title dictionary of images
        title_file = "\up_arrow.png"
        self.__titleItems = {}
        for item in self.__letterDictionary:
            self.__titleItems[item] = pygame.image.load(fileLocs.images+title_file).convert_alpha()        

        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()
        self.__splash_buttonsImage = pygame.image.load(button_file).convert_alpha()
        
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

              #scale the note
            note_x, note_y = self.__noteImage.get_size()
            note_x = int(note_x * transform)
            note_y = int(note_y * transform)
            self.__noteImage = pygame.transform.scale( self.__noteImage, (note_x, note_y))
            
             #scale the buttons
            button_x, button_y = self.__splash_buttonsImage.get_size()
            button_x = int(button_x * transform)
            button_y = int(button_y * transform)
            self.__splash_buttonsImage = pygame.transform.scale(self.__splash_buttonsImage, (button_x, button_y))
            
              #scale the title
            for item, image in self.__titleItems.iteritems():
                item_x, item_y = self.__titleItems[item].get_size()
                item_x = int( item_x * transform )
                item_y - int( item_y * transform )
                self.__titleItems[item] = pygame.transform.scale(self.__titleItems[item], (item_x, item_y))

        self.__bkgrd_x = screen_x - self.__bkgrd_rightImage.get_width()
        self.__bkgrd_y = screen_y - self.__bkgrd_rightImage.get_height()
        self.__button_y = int(screen_y / 2)
        self.__button_x = (screen_x - self.__splash_buttonsImage.get_size()[0])/2

    def __loadAudio(self):
        """
            Loads voice and sound effects files for this menu.
        """
        fileLocs=FileLocations()
        themeSongFilename="\People_Like_Us_and_Ergo_Phizmiz_-_Social_Folk_Dance.ogg"
        self.__welcomeMessage=pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_05_01.ogg")
        
          ##time file for beats
        timefile = fileLocs.beats+r"\People_Like_Us_and_Ergo_Phizmiz_-_Social_Folk_Dance.times"

        self.__times = [ float(t.strip()) for t in file(timefile, 'rt') ]
         
        self.__music = pygame.mixer.music
        self.__music.load(fileLocs.songs+themeSongFilename)
          
#        self.__buzzer = pygame.mixer.Sound(fileLocs.soundEffects+"\\fx_00_00.ogg")
        self.__narrationChannel = pygame.mixer.Channel(0)

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
        
    def __getFPS(self):
        """
           Calculates rough framerate based on number of frames displayed in previous second
        """
        self.__framesCounted = self.__framesCounted + 1
        if pygame.time.get_ticks() > (self.__timeOld + 1000):
            self.__timeOld = pygame.time.get_ticks()
            self.__framerate = self.__framesCounted
            self.__framesCounted = 0
        return self.__framerate
        
    def drawSplashMenu(self):
        """
           Draws menu to screen.  Shows image and asks player about tutorial.
        """
        notDone=True
        
        self.__soundController = SoundEffectController()
        self.__soundController.queueSound( self.__welcomeMessage )
        
        self.__controllerUpdate = False

        self.__music.play()

        while notDone:
            if self.__controllerUpdate == False and self.__music.get_pos() > 3000:
                self.__controllerUpdate = True
                self.__soundController.update()

            self.__screen.fill((74, 83, 71))
            
            for events in pygame.event.get():
                
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_ESCAPE:
                        endCredits = EndCreditsScreen( self.__screen )
                        endCredits.drawEndCredits()
                        exit() 
                if not(self.__cntrl.checkEvent(events) == None):
                    notDone = self.__checkNavEvent((self.__cntrl.checkEvent(events, 42))) #42 is fake--time doesn't matter in navigation
            """
            event = pygame.event.poll()
            if not(self.__cntrl.checkEvent(event) == None):
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            """
            yChange = 0
            
            self.__screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
            self.__screen.blit(self.__font.render(str("FPS: " + self.__getFPS().__str__()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
            self.__screen.blit(self.__splash_buttonsImage, (self.__button_x, self.__button_y))
       
            for index, item in self.__titleItems.iteritems():
#                self.__screen.blit( self.__titleItems[index], self.__letterDictionary[index].getCoords())
                self.__screen.blit(self.__font.render(index.lower(), True, self.__font_color), self.__letterDictionary[index].getCoords()) 
            
            pygame.display.flip()
            self.__sleep()
            self.__updateTitle()
        
        return True  #no expected output from this menu
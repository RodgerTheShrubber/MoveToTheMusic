"""
   The End Credits Screen displays names of people involved in the MtM project.  It uses the same Bouncer
   object as the SplashMenu to add some visual interest.  The player can hit any square on the mat to 
   exit the screen and quit the game completely.
"""

"""
   Begun 22 April by Jason Cisarano   -- includes visual elements, needs audio reading of names
   26 April updated with latest song names
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
from Bouncer import Bouncer
from bisect import bisect

class EndCreditsScreen (object):
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

        self.__nameState = 0
        self.__selected = 0
        self.__font_size = self.__chooseFontSize()
        self.__font = pygame.font.SysFont("arial", self.__font_size)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
           #initialize menus and set starting menu to main
        self.__initTitle()
        self.__loadAudio()
               
        self.__loadImages()
             
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
        self.__thanks_to = ["Diane Pozefsky","Gary Bishop"]
        self.__team = ["Trey Brumley","Jason Cisarano","Kevin Coletta","Zach Swartz"]
        self.__others = ["Luke Woodcock", "Walter Storholt"]
        self.__song_creds = ["People Like Us - \"Social Folk Dance\"", "Jonathan Coulton - \"Code Monkey\"", "The Gold State - \"Whole Wide Whole\""]
        self.__song_creds1 = ["Ditto Ditto - \"Ditto Ditto\"","yellowjacket osx - \"Nadeya (Tribal Bump Mix)\"","Loveshadow -\"Sleeping Alone\""]
        self.__song_creds2 = ["Loveshadow - \"The Sweetest Sin\"","George Ellinas - \"Best Friend Remix\"", "Andrew MAze - \"Identity of Self\""]
        screenwidth, screenheight = self.__screen_size
        titlewidth = screenwidth - int(screenwidth * 0.2) ##add some buffer on either side of title
        letterspace = int(titlewidth/self.__title.__len__() +1)
        title_y = int(screenheight * 0.3) ##place in top third of screen
        self.__letterDictionary = {}
        for c in self.__title:
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
           Any goodstep item will quit game.
        """
        self.__music.fadeout(4000)
        return False
    
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

    def __chooseFontSize(self):
        if (self.__screen_size == (1280, 960)):
            return 48
        elif (self.__screen_size == (1024, 768)):
            return 38
        elif (self.__screen_size == (800, 600)):
            return 30
     
    def __drawNames(self, screenInUse ):
        x_div = 8
        if self.__nameState == 0:
            screenInUse.blit(self.__font.render("thanks to", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, self.__screen_size[1]/2))
            for name in self.__thanks_to:
                screenInUse.blit(self.__font.render(name, True, self.__font_color), 
                                 (self.__screen_size[0]/x_div, 
                                      self.__screen_size[1]/2 + self.__font_height * (self.__thanks_to.index(name) + 2)  ) ) 
            if pygame.time.get_ticks() - self.__nameStateTime > 4000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 1
        
        if self.__nameState == 1:
            screenInUse.blit(self.__font.render("art contributed by", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, self.__screen_size[1]/2))
            screenInUse.blit(self.__font.render(self.__others[0], True, self.__font_color), 
                             (self.__screen_size[0]/x_div, 
                                  self.__screen_size[1]/2 + self.__font_height  ) )
            
            screenInUse.blit(self.__font.render("voice recordings by", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, 
                                  self.__screen_size[1]/2 + self.__font_height *3 ))
            screenInUse.blit(self.__font.render(self.__others[1], True, self.__font_color), 
                             (self.__screen_size[0]/x_div, 
                                  self.__screen_size[1]/2 + self.__font_height * 4 ) )
            if pygame.time.get_ticks() - self.__nameStateTime > 4000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 2
            
        if self.__nameState == 2:
            screenInUse.blit(self.__font.render("creative commons licensed music by", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, self.__screen_size[1]/2))
            for name in self.__song_creds:
                screenInUse.blit(self.__font.render(name, True, self.__font_color), 
                                 (self.__screen_size[0]/x_div, 
                                      self.__screen_size[1]/2 + self.__font_height * (self.__song_creds.index(name) + 2)  ) )
                
            if pygame.time.get_ticks() - self.__nameStateTime > 5000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 3
 
        if self.__nameState == 3:
            screenInUse.blit(self.__font.render("creative commons licensed music by", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, self.__screen_size[1]/2))
            for name in self.__song_creds1:
                screenInUse.blit(self.__font.render(name, True, self.__font_color), 
                                 (self.__screen_size[0]/x_div, 
                                      self.__screen_size[1]/2 + self.__font_height * (self.__song_creds1.index(name) + 2)  ) )
                
            if pygame.time.get_ticks() - self.__nameStateTime > 5000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 4

        if self.__nameState == 4:
            screenInUse.blit(self.__font.render("creative commons licensed music by", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, self.__screen_size[1]/2))
            for name in self.__song_creds2:
                screenInUse.blit(self.__font.render(name, True, self.__font_color), 
                                 (self.__screen_size[0]/x_div, 
                                      self.__screen_size[1]/2 + self.__font_height * (self.__song_creds2.index(name) + 2)  ) )
                
            if pygame.time.get_ticks() - self.__nameStateTime > 5000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 5

        if self.__nameState == 5:
            screenInUse.blit(self.__font.render("13 million triangles is", True, self.__font_color), 
                             (self.__screen_size[0]/x_div, self.__screen_size[1]/2))
            for name in self.__team:
                screenInUse.blit(self.__font.render(name, True, self.__font_color), 
                                 (self.__screen_size[0]/x_div, 
                                      self.__screen_size[1]/2 + self.__font_height * (self.__team.index(name) + 2)  ) ) 
            if pygame.time.get_ticks() - self.__nameStateTime > 8000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 6
                
        if self.__nameState == 6:
            if pygame.time.get_ticks() - self.__nameStateTime > 5000:
                self.__nameStateTime = pygame.time.get_ticks()
                self.__nameState = 0
            
            
            
        
    def drawEndCredits(self):
        """
           Draws menu to screen.  Shows image and asks player about tutorial.
        """
        notDone=True

        self.__music.play()
        
        self.__nameStateTime = pygame.time.get_ticks()

        while notDone:

            self.__screen.fill((74, 83, 71))
            event = pygame.event.poll()        
            if not(self.__cntrl.checkEvent(event) == None):
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            yChange = 0
            
            self.__screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
       
            self.__drawNames( self.__screen )
            for index, item in self.__titleItems.iteritems():
                self.__screen.blit(self.__font.render(index.lower(), True, self.__font_color), self.__letterDictionary[index].getCoords()) 
            
            pygame.display.flip()
            self.__sleep()
            self.__updateTitle()
        
        return True  #no expected output from this menu
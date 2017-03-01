"""
   LoginMenu displays menu items related to login options including add and remove accounts.
   The LoginMenu is a sub menu to IntroMenu -- IntroMenu will only create one when the player
   chooses the Login option.  Like other menus, it will loop while player makes his/her choices.
   It has built-in input controllers that need no outside initialization.
   
   When the player has completed his or her choices and selected "done," LoginMenu will return a 
   PlayerInfo object with the player's information.
"""

"""
   14 March -- complete overhaul to change over to graphical and audio elements.
   22 April -- completed logout function
"""

"""
   Navigation scheme is the same regardless of input method:
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
from PlayerProfile import PlayerProfile
from FileLocations import FileLocations
from NameEntryMenu import NameEntryMenu  

class LoginMenu (object):
    """
       LoginMenu displays menu items related to login options including add and remove accounts.
       The LoginMenu is a sub menu to IntroMenu -- IntroMenu will only create one when the player
       chooses the Login option.  Like other menus, it will loop while player makes his/her choices.
       It has built-in input controllers that need no outside initialization.
       
       When the player has completed his or her choices and selected "done," LoginMenu will return a 
       PlayerInfo object with the player's information.
    """

    def __init__(self, screen, gameInfo):
        """
           Set default values for font, menu items
        """
        self.__cntrl = Controller()
        self.__game = gameInfo
        self.__playerProfile = self.__game.getPlayer(0).getProfile()
        
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

    def __initMenus(self):
        """
           Initialize all menus needed for IntroMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems and currentMenuColors attributes.
        """
        self.__menuItems=["My Account", "Logout", "Create Account", "Delete Account", "Done"]
 
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
                return False
            
            if self.__menuItems[self.__selected] == "My Account":
                  #stub
                nameEntryMenu = NameEntryMenu(self.__screen, self.__game, "loadAccount")
                self.__playerProfile = nameEntryMenu.drawNameEntryMenu()
                nameEntryMenu = None
                return True

            if self.__menuItems[self.__selected] == "Create Account":
                nameEntryMenu = NameEntryMenu(self.__screen, self.__game, "createAccount")
                self.__playerProfile = nameEntryMenu.drawNameEntryMenu()
                nameEntryMenu = None
                return True
            
            if self.__menuItems[self.__selected] == "Delete Account":
                nameEntryMenu = NameEntryMenu(self.__screen, self.__game, "deleteAccount")
                self.__playerProfile = nameEntryMenu.drawNameEntryMenu()
                nameEntryMenu = None
                return True
            
            if self.__menuItems[self.__selected] == "Logout":
                self.__playerProfile.dispose()

        "Escape -- left arrow"
        if(step.getLocation()==(0,1)):
            return False    
        
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
        menuImage_file = fileLocs.images_menus+r"\accountmenu.png"
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        
        
        self.__menuImage = pygame.image.load(menuImage_file).convert_alpha()
        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()
        
          #settings for placement on screen  -- default items
        self.__offset_x = 80
        self.__offset_y = 50
        self.__menuItem_height = 115
        self.__menu_Y_bump = 10 #centers the note on menu item
          
        screen_x, screen_y = self.__screen_size
          #adjust dimensions according to screen size if needed
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
        self.__menuSoundsFilename=["\menu_02_01.ogg", "\menu_02_14.ogg", "\menu_02_02.ogg", "\menu_02_03.ogg", "\menu_00_01.ogg"]
        self.__menuSound=[]
        for filename in self.__menuSoundsFilename:
            self.__menuSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
        self.__narrationChannel = pygame.mixer.Channel(0)

    def __playSound(self, soundFile):
        soundValue = self.__game.getSettings().getVoiceVolume() / 100.0
        soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)
       
    def drawLoginMenu(self):
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
            self.__screen.blit(self.__noteImage, (self.__offset_x/5, self.__offset_y + (self.__selected * self.__menuItem_height) + self.__menu_Y_bump))
            self.__screen.blit(self.__font.render(str(self.__playerProfile.getPlayerName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
                        
            pygame.display.flip()
            pygame.time.wait(2)
        
        self.__screen.fill((74, 83, 71))
        return self.__playerProfile

         
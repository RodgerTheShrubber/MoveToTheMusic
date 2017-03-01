"""
   NameEntryMenu is used to allow the player to enter a login name.  It includes needed
   elements for creating a new account, accessing an old one, and for deleting an account.
   This is the one menu that doesn't use the mat for input.  Since the players are entering
   their names, they use the keyboard.  To quit this menu, players either hit ESCAPE or type
   "quit" into the name field.
   
   When the player has completed his or her choices, NameEntryMenu will return a 
   PlayerInfo object with the player's information.
"""

"""
   2 April -- began class, including loadAccount and createAccount- Jason Cisarano
   26 April -- fix for files not found
"""

import pygame
from pygame.locals import *
from GoodStep import GoodStep
from Controller import Controller
from PlayerProfile import PlayerProfile
from FileLocations import FileLocations
from SoundEffectController import SoundEffectController   

fileLocs=FileLocations()

class NameEntryMenu (object):
    """
       NameEntryMenu is used to allow the player to enter a login name.  It includes needed
       elements for creating a new account, accessing an old one, and for deleting an account.
       This is the one menu that doesn't use the mat for input.  Since the players are entering
       their names, they use the keyboard.  To quit this menu, players either hit ESCAPE or type
       "quit" into the name field.
       
       When the player has completed his or her choices, NameEntryMenu will return a 
       PlayerInfo object with the player's information.
       
       Three types of menus are supported: loadAccount, newAccount, deleteAccount
    """
    
    def __init__(self, screen, gameInfo, type):
        """
           Set default values for font, menu items
        """
        self.__cntrl = Controller()
        self.__game = gameInfo
        self.__player = self.__game.getPlayer(0).getProfile()
        self.__alphabet = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.__alphabet_size = len(self.__alphabet)
        
        self.__type = type
        self.__name = [0,0,0]
        self.__strName = "---"
        self.__MAX_INITIALS = len(self.__name)
        self.__onLetter = 0
        self.__gotName = False
        
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
    
    def __rename(self):
        newStr =""
        for num in self.__name:
            newStr += self.__alphabet[num]
        self.__strName = newStr
        

    def __initMenus(self):
        """
           Initialize all menus needed for IntroMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems and currentMenuColors attributes.
        """
        if self.__type == "loadAccount" or self.__type == "createAccount":
            self.__menuItems=["Done"]
            
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
            if ( self.__onLetter == self.__MAX_INITIALS - 1):
                if self.__menuItems[self.__selected] == "Done":
                    return False
            else:
                self.__onLetter += 1
                
        "Choose an option logic -- left arrow"   
        if(step.getLocation()==(0, 1)):
            if ( self.__onLetter == 0):
                if self.__menuItems[self.__selected] == "Done":
                    return False
            else:
                self.__onLetter -=1
        
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        menuImage_file = fileLocs.images_menus+r"\accountmenu.png"
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
        self.__menuSoundFilename = { "done":"\menu_00_01.ogg", "retry":"\menu_02_09.ogg", "back":"\menu_02_06.ogg" }
        if self.__type == "loadAccount":
            self.__menuSoundFilename["prompt"] = "\menu_02_05.ogg"
            self.__menuSoundFilename["success"] = "\menu_02_11.ogg"
            self.__menuSoundFilename["failure"] = "\menu_02_07.ogg"
        if self.__type == "createAccount":
            self.__menuSoundFilename["prompt"] = "\menu_02_04.ogg"
            self.__menuSoundFilename["success"] = "\menu_02_10.ogg"
            self.__menuSoundFilename["failure"] = "\menu_02_08.ogg"
        if self.__type == "deleteAccount":
            self.__menuSoundFilename["prompt"] = "\menu_02_12.ogg"
            self.__menuSoundFilename["success"] = "\menu_02_13.ogg"
            self.__menuSoundFilename["failure"] = "\menu_02_07.ogg"
            
          ###load sounds
        self.__menuSound = {}
        for type, filename in self.__menuSoundFilename.iteritems():
            self.__menuSound[type] = pygame.mixer.Sound(fileLocs.menuSounds+filename)
            
        self.__narrationChannel = pygame.mixer.Channel(0)

    def __playSound(self, soundFile):
        soundValue = self.__game.getSettings().getVoiceVolume() / 100.0
        soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)
    
    def __getLoginName(self, screen):
        """ask(screen, question) -> answer
           getLoginName and displayBox based on ask() and displayBox()
           by Timothy Downs (http://mu.arete.cc/pcr/syntax/textinput/1/textinput.py)
        """
        current_string = ""
        self.__display_box(screen, "")
        
        soundController = SoundEffectController()        
        self.__playSound(pygame.mixer.Sound(fileLocs.nameEntry+r"\menu_12_01.ogg"))
        self.__playSound(pygame.mixer.Sound(fileLocs.nameEntry+r"\menu_12_02.ogg"))
        print 'played'
        soundController.update()
        soundController.update()
        
        while True:
            soundController.update()
            event = pygame.event.wait()
            if event.type == QUIT:
                break
            if event.type != KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                current_string = "quit"
                return "quit"
            if event.key == K_BACKSPACE:
                current_string = current_string[:-1]
            elif event.key == K_RETURN:
                self.__gotName = True
                break
            step=self.__cntrl.checkEvent(event, 42)
            
            """Down arrow"""
            if(step.getLocation()==(1, 0)):
                if (self.__name[self.__onLetter] == 0 ):
                    self.__name[self.__onLetter] = self.__alphabet_size - 1
                else:
                    self.__name[self.__onLetter] = self.__name[self.__onLetter] - 1
                self.__playSound(pygame.mixer.Sound(self.__player.ALPH_DICT[self.__alphabet[self.__name[self.__onLetter]]]))
            
            "Scroll up logic -- up arrow"
            if(step.getLocation()==(1, 2)):
                if (self.__name[self.__onLetter] == self.__alphabet_size - 1 ):
                    self.__name[self.__onLetter] = 0
                else:
                    self.__name[self.__onLetter] = self.__name[self.__onLetter] + 1
                self.__playSound(pygame.mixer.Sound(self.__player.ALPH_DICT[self.__alphabet[self.__name[self.__onLetter]]]))
        
            self.__rename()
            
            "Choose an option logic -- right arrow"
            if(step.getLocation()==(2, 1)):
                if ( self.__onLetter == self.__MAX_INITIALS - 1):
                    self.__gotName = True
                    break
                else:
                    self.__onLetter += 1
                    if ( self.__onLetter == self.__MAX_INITIALS - 1):
                        self.__playSound(pygame.mixer.Sound(fileLocs.nameEntry+r"\menu_12_03.ogg"))
                    
                
            "Choose an option logic -- left arrow"   
            if(step.getLocation()==(0, 1)):
                if ( self.__onLetter == 0):
                    return "quit"
                else:
                    self.__onLetter -=1
            self.__display_box(screen, current_string)
            
        return self.__strName

    def __display_box(self, screen, message, fgcolor=(244, 123, 25), bgcolor=(74, 83, 71)):
        "Print a message in a box in the middle of the screen"
        fontobject = pygame.font.SysFont("arial", 72 )
        font_height = fontobject.get_linesize()
        area = Rect(0, 0, 200, font_height)
        area.center = screen.get_rect().center
        pygame.draw.rect(screen, bgcolor, area, 0)
        pygame.draw.rect(screen, fgcolor, area, 3)
        oldclip = screen.get_clip()
        screen.set_clip(area.inflate(-4, -4))
        text1 = fontobject.render(self.__strName, 1, fgcolor, bgcolor)
        screen.blit(text1, area.move(5, 4))
        if len(message):
            text1 = fontobject.render(message, 1, fgcolor, bgcolor)
            screen.blit(text1, area.move(5, font_height + 15))

        screen.set_clip(oldclip)
        pygame.display.update(area)
       
    def drawNameEntryMenu(self):
        """
           Draws text entry box to screen and waits for user input.  Then it tries to use that login
           name to load or create a player profile as appropriate.
        """
        notDone=True
#        soundController = SoundEffectController()

        while notDone:
            self.__screen.fill((74, 83, 71))
            event = pygame.event.wait()        
            if not(self.__cntrl.checkEvent(event) == None):
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            yChange = 0
            
            self.__screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
            self.__screen.blit(self.__menuImage, (self.__offset_x, self.__offset_y))
#            self.__screen.blit(self.__noteImage, (self.__offset_x/5, self.__offset_y + (self.__selected * self.__menuItem_height) + self.__menu_Y_bump))
            self.__screen.blit(self.__font.render(str(self.__player.getPlayerName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
            pygame.display.flip()

            while not self.__gotName:
                  #only play the first time through
#                if not self.__narrationChannel.get_busy():
#                    self.__playSound(self.__menuSound["prompt"])
 
#                soundController.queueSound( self.__menuSound["prompt"])
#                soundController.queueSound(["back"])
#                soundController.update()
                
                if self.__type == "createAccount":
                    name = self.__getLoginName(self.__screen)
                    if name == "quit" or name == "":
#                        self.__playSound(self.__menuSound["back"])
                        break
                    self.__gotName = self.__player.setNewPlayerName(name)
                    
                if self.__type == "loadAccount":
                    name = self.__getLoginName(self.__screen)
                    if name == "quit" or name == "":
#                        self.__playSound(self.__menuSound["back"])
                        break
                    if self.__player.setExistingPlayerName( name ):
                        self.__gotName = True
                        self.__player.loadPlayerFile()
                    else:
                        self.__gotName = False
                        
                if self.__type == "deleteAccount":
                    name = self.__getLoginName(self.__screen)
                    if name == "quit" or name == "":
#                        self.__playSound(self.__menuSound["back"])
                        break
                    if name == self.__player.getPlayerName():
                          #can't delete logged-in profile
                        break
                    temp = PlayerProfile()
                    if temp.setExistingPlayerName( name ):
                        self.__gotName = temp.deleteThisPlayerProfile()
                    else:
                        self.__gotName = False
                
                  #play result messages
                if self.__gotName:
                      #play success message
                    self.__playSound(self.__menuSound["success"])
                else:
                      #play failure message
                    self.__playSound(self.__menuSound["failure"])
            pygame.time.wait(2)
            notDone = False
        
        self.__screen.fill((74, 83, 71))
        return self.getPlayerInfo()

    def getPlayerInfo(self):
        """
           Returns player profile.
        """
        return self.__player
         
"""
   SongChooserMenu displays a list of songs appropriate for the player's current status in
   the game and allows her to choose a song to play.  It takes a GameInfo item as input and
   returns a song file.
   
   this class is usable with both freeplay and challenge mode levels.
"""

"""
   6 April -- Begun by Jason Cisarano -- Completed "freeplay" song chooser with text-only, no-audio interface
               "career" mode interface displays songs and available levels, but doesn't allow user to choose
               song yet.
   26 April -- added filenames and titles for new songs
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
from GoodStep import GoodStep
from Controller import Controller
from GameInfo import GameInfo
from FileLocations import FileLocations
from GameOverScreen import GameOverScreen
from SoundEffectController import SoundEffectController
import SinglePlayerMode
import CareerMode    

class ScreenInfo():
    """
       Holds standard info about display including font and font size.
    """
    pygame.init()
    game = GameInfo()
    SCREEN_SIZE = game.getSettings().getScreenSize()
    font = pygame.font.SysFont("arial", 16);
    font_height = font.get_linesize()

class SongChooserMenu (object):
    """
       SongChooserMenu displays a list of songs appropriate for the player's current status in
       the game and allows her to choose a song to play.  It takes a GameInfo item as input and
       returns a song file.
       
       SongChooserMenu adjusts its output for freeplay and challenge mode levels.
    """
       
    def __init__(self, screen, gameInfo):
        """
           Set default values for font, menu items
           Parameters: screen is current screen in use
                       gameInfo is up-to-date GameInfo object
        """
        self.__game = gameInfo
        self.__cntrl = Controller()
        self.__selectedSong = ""
        
        self.__screen = screen
        self.__screen_size = screen.get_size()
        self.__screenInfo = ScreenInfo()
        self.__soundEffects = SoundEffectController()

        self.__font_size = self.__chooseFontSize()
        self.__font = pygame.font.SysFont("arial", self.__font_size)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        print self.__font_height
             
        self.__selected = 0
        
          #initialize menus and set starting menu to main
        self.__initMenus()
        self.__loadAudio()
        self.__loadImages()

    def __initMenus(self):
        """
           Initialize all menus needed for IntroMenu navigation.  These menus are used indirectly by main
           program's currentMenuItems and currentMenuColors attributes.
        """
        self.__menuItems=["Login", "Play", "Single Player", "Multiplayer", "Setup", "Quit"]

        self.__songTitles={"1":(("TeQuieroMas", "\TeQuieroMas"), ("Ditto Ditto", "\ditto_ditto")), 
                           "2":(("Identity of Self", "\identity"), ("Whole Wide Whole", "\WholeWideWhole")), 
                           "3":(("Code Monkey", "\CodeMonkey"), ("Nadeya", "\\nadeya")), 
                           "4":(("DNA Funkdafied Mix", "\dna"), ("Best Friend Remix", "\\best_friend")), 
                           "5":(("Sleeping Alone", "\sleeping_alone"), ("The Sweetest Sin", "\sweetest_sin"))}

        self.__songTitle_filenames = { 
                            "TeQuieroMas":"\menu_10_00.ogg", "Ditto Ditto": "\menu_10_02.ogg", 
                            "Identity of Self" : "\menu_10_01.ogg", "Whole Wide Whole" : "\menu_10_03.ogg", 
                            "Code Monkey" : "\menu_10_04.ogg", "Nadeya" : "\menu_10_05.ogg", 
                            "DNA Funkdafied Mix" : "\menu_10_06.ogg", "Best Friend Remix" : "\menu_10_07.ogg", 
                            "Sleeping Alone" : "\menu_10_08.ogg", "The Sweetest Sin" : "\menu_10_09.ogg"}

        self.__levelSongs = {}        
        if self.__game.getGameMode() == "career":
              #make dictionary of levels player has unlocked
            self.__availableLevels = {}
            for level in self.__songTitles.iterkeys():
                if int(level) <= self.__game.getPlayer(0).getProfile().getLevelReached():
                    self.__availableLevels[level] = self.__songTitles[level]
            
            self.__selectMode = "chooseLevel"
            
              #init with level 1 songs -- assumes only 2 songs per level
            song1, song2 = self.__songTitles["1"]
            self.__levelSongs[2] = song1
            self.__levelSongs[1] = song2
            self.__levelSongs[0] = ("Back", "")
            
        else:
            self.__selectMode = "chooseSong"
            index = 0
            for level in self.__songTitles.iterkeys():
                song1, song2 = self.__songTitles[level]
                self.__levelSongs[index +1] = song2
                self.__levelSongs[index] = song1
                index = index + 2 
        
    def __checkNavEvent(self, step):
        """
           Looks at GoodStep item, updates self.selected as appropriate.
        """
        if self.__selectMode == "chooseLevel":
            length = self.__availableLevels.__len__()
        else:
            length = len(self.__levelSongs)

        "Scroll down logic -- down arrow"
        if(step.getLocation()==(1, 0)):
              #update selected
            self.__selected += 1
            if length-1 < self.__selected:
                self.__selected = 0
            self.__playMenuItemSound()
            
        "Scroll up logic -- up arrow"
        if(step.getLocation()==(1, 2)):
              #update selected
            self.__selected -= 1
            if self.__selected < 0:
                self.__selected = length-1
            self.__playMenuItemSound()
        
        "Choose an option logic -- right arrow"
        if(step.getLocation()==(2, 1)):
            if (self.__selectMode == "chooseLevel"):
                  #convert all elements to "choose song"
                self.__game.setCurrentLevel(self.__selected + 1)  #sets current level
                song1, song2 = self.__songTitles[(self.__selected + 1).__str__()]
                self.__levelSongs[2] = song1
                self.__levelSongs[1] = song2
                self.__selected = 0
                self.__selectMode = "chooseSong"
                self.__playSound(self.__pickSong)
                self.__noteStart_y = self.__offset_y + self.__songList_y
                #self.__noteStart_y = self.__songList_y + self.__font_height
                return True 
            else:
                if self.__levelSongs[self.__selected][0] == "Back":
                    self.__selectMode = "chooseLevel"
                    self.__noteStart_y = self.__offset_y + 2*self.__font_height
                    #self.__noteStart_y = self.__offset_y + 2*self.__font_height
                    self.__playSound(self.__pickLevel)
                    self.__selected = 0
                    return True
                else:
                    self.__selectedSong = self.__levelSongs[self.__selected]
                    self.__game.setCurrentSong(self.__selectedSong)
                    if self.__game.getGameMode() == "freeplay":
                        lastGameInfo=SinglePlayerMode.startGame(self.__screen, self.__screenInfo, self.__game)
                    elif self.__game.getGameMode() == "career":
                        lastGameInfo=CareerMode.startGame(self.__screen, self.__screenInfo, self.__game)
                    
                    self.__game = lastGameInfo
                    self.backFromSong = True
                    gameOverScreen = GameOverScreen(self.__screen,self.__game)
                    gameOverScreen.drawScreen(self.__screenInfo, self.__game, self.__soundEffects)
                    gameOverScreen = None
                    self.__playSound(self.__returnMessage)
                    return True
        
        "Escape -- left arrow"
        if(step.getLocation()==(0, 1)):
            return False
        
        return True
  
    def __loadImages(self):
        """
            Loads images for menus, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
        menuImage_file = fileLocs.images_menus+r"\songChooserMenu.png"
        note_file = fileLocs.images_menus+r"\note.png"
        menu_bkgrd_file = fileLocs.images_menus+r"\menu_right.png"
        
        self.__menuImage = pygame.image.load(menuImage_file).convert_alpha()
        self.__noteImage = pygame.image.load(note_file).convert_alpha()
        self.__bkgrd_rightImage = pygame.image.load(menu_bkgrd_file).convert_alpha()
        
          #scale note to match font height
        note_x, note_y = self.__noteImage.get_size()
        self.__noteImage = pygame.transform.scale(self.__noteImage, (note_x, self.__font_height))
        
          #settings for placement on screen  -- default items
        self.__offset_x = 80
        self.__offset_y = 50
        self.__menuItem_height = self.__font_height
        self.__menu_Y_bump = 10 #centers the note on menu item
          
        screen_x, screen_y = self.__screen_size
        
          #scale image dimensions according to screen size if needed
        if(screen_x != 1280):
            transform = 0
            if(screen_x == 800):
                transform = 0.625
            elif(screen_x == 1024):
                transform = 0.8
            self.__offset_x = self.__offset_x * transform
             
#            menu_x, menu_y = self.__menuImage.get_size()
#            menu_x = int(menu_x * transform)
#            menu_y = int(menu_y * transform)
            note_x, note_y = self.__noteImage.get_size()
            note_x = int(note_x * transform)
            note_y = int(note_y * transform)
#            self.__menuImage = pygame.transform.scale( self.__menuImage, (menu_x, menu_y))
            self.__noteImage = pygame.transform.scale(self.__noteImage, (note_x, note_y))
        
          #level list only displays in career mode    
        if self.__game.getGameMode() == "career":
            self.__songList_y = self.__offset_y  + (self.__font_height * 7)
            self.__noteStart_y = 2* self.__offset_y + self.__font_height
        else:
            self.__songList_y = self.__offset_y + self.__font_height
            self.__noteStart_y = self.__offset_y + self.__songList_y #+ 2*self.__font_height

        self.__bkgrd_x = screen_x - self.__bkgrd_rightImage.get_width()
        self.__bkgrd_y = screen_y - self.__bkgrd_rightImage.get_height()
        
    def __loadAudio(self):
        """
            Loads voice and sound effects files for this menu.
        """
        fileLocs=FileLocations()
        self.__menuSoundsFilename=["\menu_01_01.ogg", "\menu_01_02.ogg", "\menu_01_03.ogg", "\menu_01_04.ogg", "\menu_01_05.ogg", "\menu_01_06.ogg"]
        self.__menuSound=[]
        for filename in self.__menuSoundsFilename:
            self.__menuSound.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
        
        self.__songTitleAudio = {}
        for title, filename in self.__songTitle_filenames.iteritems():
            self.__songTitleAudio[title] = pygame.mixer.Sound(fileLocs.menuSounds+filename) 
         
        self.__levelNumber = []       
        self.__levelNumberFilename = ["\menu_09_04.ogg", "\menu_09_05.ogg", "\menu_09_06.ogg", "\menu_09_07.ogg", "\menu_09_08.ogg"]
        for filename in self.__levelNumberFilename:
            self.__levelNumber.append(pygame.mixer.Sound(fileLocs.menuSounds+filename))
                                 
          #one-off sounds
        self.__diffLevel = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_09_09.ogg")
        self.__pickSong = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_09_01.ogg")
        self.__pickLevel = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_09_02.ogg")
        self.__returnMessage = pygame.mixer.Sound(fileLocs.menuSounds+r"\menu_09_03.ogg")   
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

    def __playMenuItemSound(self):
        """
           Chooses a song title or level number to play based on current mode.
        """
        if self.__selectMode == "chooseSong":
            if self.__levelSongs[self.__selected][0] != "Back": 
                self.__playSound(self.__songTitleAudio[self.__levelSongs[self.__selected][0]])
            else:
                self.__playSound(self.__diffLevel)
        elif self.__selectMode == "chooseLevel":
            self.__playSound(self.__levelNumber[(self.__selected)])
        
    def __chooseFontSize(self):
        if (self.__screen_size == (1280, 960)):
            return 48
        elif (self.__screen_size == (1024, 768)):
            return 38
        elif (self.__screen_size == (800, 600)):
            return 30


    def drawSongChooserMenu(self, screen):
        """
           Draws menu to screen.  Takes control of game while menus are displayed.
           Menu can change based on menu level (some items have sub-levels) and 
           what item is selected.  Currently selected item is highlighted.
           Param is screen currently in use.
        """
        notDone=True
        firstTime=True
        self.backFromSong=False

        if self.__game.getGameMode() == "career":
            self.__playSound(self.__pickLevel)
        else:
            self.__playSound(self.__pickSong)
            
        while notDone:
            if self.backFromSong == True:
                self.__initMenus()
                self.__noteStart_y = self.__offset_y + 2*self.__font_height
                self.__selected = 0
                self.backFromSong = False
            
            self.__screen.fill((74, 83, 71))
            event = pygame.event.wait()   
            if not(self.__cntrl.checkEvent(event) == None):
                self.__statusPlaying = False
                notDone = self.__checkNavEvent((self.__cntrl.checkEvent(event, 42))) #42 is fake--time doesn't matter in navigation
            yChange = 0
            
#            screen.blit(self.__menuImage, (self.__offset_x, self.__offset_y))            
            screen.blit(self.__bkgrd_rightImage, (self.__bkgrd_x, self.__bkgrd_y))
              #menu note
            screen.blit(self.__noteImage, (self.__offset_x, self.__noteStart_y + (self.__selected * self.__menuItem_height)))
            
            screen.blit(self.__font.render("Current mode: "+str(self.__game.getGameMode()), True, self.__font_color), (self.__offset_x, self.__offset_y))

            if self.__game.getGameMode() == "career":
                screen.blit(self.__font.render("Choose a Level: ", True, self.__font_color), (self.__offset_x, self.__offset_y + self.__font_height))
                for level in self.__availableLevels:
                    screen.blit(self.__font.render("Level "+level, True, self.__font_color), 
                                (self.__offset_x * 2, self.__offset_y + (self.__font_height * 2 + (self.__font_height * (int(level)-1)))))
                
            screen.blit(self.__font.render("Choose a song: ", True, self.__font_color), (self.__offset_x, self.__songList_y))
            for index in self.__levelSongs:
                screen.blit(self.__font.render(str(self.__levelSongs[index][0]), True, self.__font_color), 
                            (self.__offset_x * 2, self.__offset_y  + self.__songList_y + (self.__font_height* int(index))))

            screen.blit(self.__font.render(str(self.__game.getPlayer(0).getName()), True, self.__font_color), (0, self.__screen_size[1] - self.__font_height -5))
                        
            pygame.display.flip()
            pygame.time.wait(5)

        self.__screen.fill((74, 83, 71))
        print self.__selectedSong
        return self.getSelectedSong()

    def getSelectedSong(self):
        """
           Returns game info as determined by user input.
        """
        return self.__selectedSong
    
         
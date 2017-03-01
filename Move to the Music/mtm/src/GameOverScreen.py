"""
  GameOverScewwn draws the screen that players will see when they finish the game
"""

"""
   Created 17 February by Trey Brumley. Draws basic Game over screen
"""

"""
   Border looks like this
   =======================================
   |    CONGRATULATIONS, <NAME>          |
   |  =========== ========== ==========  |
   | | HIGH    |  | GAME   | | HIGH   |  |
   | | SCORES  |  | OVER   | | SCORES |  |
   | | (PLAYER)|  | SCREEN | | (SONG) |  |
   | ===========  ========== ==========  |
   |   YOU SCORED  <POINTS> POINTS!!     |
   |-------------------------------------|
   | * LIST PLAYER HIGH SCORES           |
   |   LIST SONG HIGH SCORES             |
   |   DONE                              |
   =======================================
"""

import pygame
from pygame.locals import *
from FileLocations import FileLocations
from SoundEffectController import SoundEffectController
from HighScores import HighScores
from Controller import Controller

    
global highScores
highScores=HighScores()
highScores.loadSongScores()
global fileLocs
fileLocs=FileLocations()

class GameOverScreen (object):
    
    def __init__(self, screen,gameInfo):
        """
           Set default values for font, menu items
        """
        self.__game = gameInfo
        self.__player1 = gameInfo.getPlayer(0)
        self.__stats = self.__player1.getGameStats()
        self.__settings = self.__game.getSettings()
        
    
        
        self.__screen = screen
        self.__screen_size = screen.get_size()
        self.__danceFloorCounter = 0
        self.__danceFloorArray = []
        
        self.__loadImages()
        
        self.lastMoves=[]
        
            
        
        self.__selected = 0
        self.__soundEffects = SoundEffectController()
        self.__done= pygame.mixer.Sound(fileLocs.menuSounds+"\menu_00_01.ogg")
        self.__playHighScores=pygame.mixer.Sound(fileLocs.menuSounds+"\menu_00_01.ogg")
        self.__myHighScores=pygame.mixer.Sound(fileLocs.menuSounds+"\menu_00_01.ogg")
        
        self.__font = pygame.font.SysFont("arial", 48)
        self.font = pygame.font.SysFont("arial", 48)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
        self.__narrationChannel = pygame.mixer.Channel(0)
        
    def __playSound(self, soundFile):
        """
           Plays soundFile on __narrationChannel.  Only one sound can be played at a time
           and subsequent sounds will override one another.
        """
        #soundValue = self.__gameSettings.getVoiceVolume() / 100.0
        #soundFile.set_volume(soundValue)
        self.__narrationChannel.play(soundFile)
        
    def __checkNavEvent(self, step):
        """
           Looks at GoodStep item, updates self.selected as appropriate.
        """
        max = 2
        if(str(self.__player1.getName())!="New player"):
            top_scores = highScores.getScoresForSong(str(self.__game.getCurrentSong()))
            player_scores = highScores.getScoresForPlayer(str(self.__player1.getName()),str(self.__game.getCurrentSong()))
            

        "Scroll down logic -- down arrow"
        if(step.getLocation()==(1, 0)):
            if(str(self.__player1.getName())!="New player"):
                self.__selected += 1
                if max < self.__selected:
                    self.__selected = 0
                self.__playMenuItemSound()
            
        "Scroll up logic -- up arrow"
        if(step.getLocation()==(1, 2)):
            if(str(self.__player1.getName())!="New player"):
                self.__selected -= 1
                if self.__selected < 0:
                    self.__selected = max
                self.__playMenuItemSound()
        
        "Choose an option logic -- right arrow"
        if(step.getLocation()==(2, 1)):
            if (self.__selected == 0):
                return False 
            elif (self.__selected==1):
                index=1
                if(str(self.__player1.getName())!="New player"):
                    for i in top_scores:

                        theName =str(highScores.top_song_scores[str(self.__game.getCurrentSong())][i])
                        theIndex =0
        
                        if (theName == "???"):
                            self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.alphSounds+r"\menu_11_28.ogg"))
                        else :
                            while theIndex <3:
                                self.__soundEffects.queueSound(pygame.mixer.Sound(self.__player1.profile.ALPH_DICT[theName[theIndex]]))
                                theIndex +=1
                        self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.scoring+r"\menu_13_01.ogg"))
                        self.__soundEffects.playNumberSound(str(i))
                        self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.scoring+r"\menu_13_02.ogg"))
                        self.__soundEffects.playAllSounds()
                        index+=1
                return True
            else:
                index=1
                if(str(self.__player1.getName())!="New player"):
                    for i in player_scores:
                        theName = str(highScores.players_top_scores[str(self.__player1.getName())][str(self.__game.getCurrentSong())][i])
                        theIndex =0
        
                        if (theName == "???"):
                            self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.alphSounds+r"\menu_11_28.ogg"))
                        else :
                            while theIndex <3:
                                self.__soundEffects.queueSound(pygame.mixer.Sound(self.__player1.profile.ALPH_DICT[theName[theIndex]]))
                                theIndex +=1
                        self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.scoring+r"\menu_13_01.ogg"))
                        self.__soundEffects.playNumberSound(str(i))
                        self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.scoring+r"\menu_13_02.ogg"))
                        self.__soundEffects.playAllSounds()
                        index+=1
                return True
        
        "Escape -- left arrow"
        if(step.getLocation()==(0, 1)):
            return False
        
        return True

    def __playMenuItemSound(self):
        if(self.__selected==0):
            self.__playSound(self.__done)
        elif(self.__selected==1):
            dummy= 0
            
        else:
            
            dummy= 0
        
    def transformImage(self,img):
        screen_x,screen_y = self.__screen_size
        if(screen_x != 1280):
            transform = 0
            if(screen_x == 800):
                transform = 0.625
            elif(screen_x == 1024):
                transform = 0.8
            img_x, img_y = img.get_size()
            img_x = int(img_x * transform)
            img_y = int(img_y * transform)
            img = pygame.transform.scale( img, (img_x, img_y))
        return img
        
    
    def __loadImages(self):
        """
            Loads images for arrows, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
            #load the arrow files
        game_over_file = fileLocs.images+r"\game_over.png"
        self.__game_over = pygame.image.load(game_over_file).convert_alpha()
        font = pygame.font.SysFont("arial", 48)
        self.__high_song_score =font.render("Song High Scores", True, (0, 0, 0))
        self.__high_player_score =font.render("Player High Scores", True, (0, 0, 0))
        
        
        self.__margin_x = 15
        self.__margin_y = 15
        self.__offset_x = 80
        self.__offset_y = 75
        self.__menuItem_height = 100
        self.__menu_Y_bump = 10
          #must eventually allow for different sized screens
        self.screen_x, self.screen_y = self.__screen_size
        
    def drawScreen(self, screenInf,currentGame, soundEffects):
        """
           Draws visual elements to screen.  Draws the string representation of how to win
        """
        highScores.loadSongScores()
        if(currentGame.getPlayer(0).getName()!='New player'):
            highScores.updateHighScores( str(currentGame.getPlayer(0).getName()), str(currentGame.getCurrentSong()),int(currentGame.getPlayer(0).getGameStats().getCurrentScore()))   
            highScores.updatePlayerHighScores( str(currentGame.getPlayer(0).getName()), str(currentGame.getCurrentSong()),int(currentGame.getPlayer(0).getGameStats().getCurrentScore()))  
        highScores.saveSongScores()
        
        self.__screen.fill((255, 255, 255))      
        
            #display diagonal arrows
        self.__game_over = self.transformImage(self.__game_over)
        image_x, image_y = self.__game_over.get_size()
        screen_x, screen_y = self.__screen_size
        self.__screen.blit(self.__game_over, ((screen_x-image_x)/2+self.__margin_x,(screen_y-image_y)/2))
        
        top_part = self.font.render("CONGRATULATIONS, "+str(currentGame.getPlayer(0).getName()), True, (0, 0, 0))
        bottom_part = self.font.render("YOU SCORED "+str(currentGame.getPlayer(0).getGameStats().getCurrentScore())+" POINTS!!!", True, (0, 0, 0))
        
        theName =str(currentGame.getPlayer(0).getName())
        
        theIndex =0
        
        if (theName == "???"):
             self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.alphSounds+r"\menu_11_28.ogg"))
        else :
            while theIndex <3:
                self.__soundEffects.queueSound(pygame.mixer.Sound(self.__player1.profile.ALPH_DICT[theName[theIndex]]))
                theIndex +=1
        self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.scoring+r"\menu_13_01.ogg"))
        self.__soundEffects.playNumberSound(str(currentGame.getPlayer(0).getGameStats().getCurrentScore()))
        self.__soundEffects.queueSound(pygame.mixer.Sound(fileLocs.scoring+r"\menu_13_02.ogg"))
        self.__soundEffects.playAllSounds()
        
        
        
        top_part = self.transformImage(top_part)
        text_x, text_y = top_part.get_size()
        self.__screen.blit(top_part,( (screen_x - text_x)/2 ,0))
        
        bottom_part = self.transformImage(bottom_part)
        text_x, text_y = bottom_part.get_size()
        self.__screen.blit(bottom_part,( (screen_x - text_x)/2 ,self.font.get_linesize()))
        soundEffects.playNumberSound(currentGame.getPlayer(0).getGameStats().getCurrentScore())
        if(str(currentGame.getPlayer(0).getName())!="New player"):
            self.__high_song_score = self.transformImage(self.__high_song_score)
            image_x, image_y = self.__high_song_score.get_size()
            self.__screen.blit(self.__high_song_score, (self.__margin_x,self.screen_y/4))
        
            self.__high_player_score = self.transformImage(self.__high_player_score)
            image_x, image_y = self.__high_player_score.get_size()
            self.__screen.blit(self.__high_player_score, (self.screen_x-self.__margin_x-image_x,self.screen_y/4))
        
            top_scores = highScores.getScoresForSong(str(currentGame.getCurrentSong()))
            player_scores = highScores.getScoresForPlayer(str(currentGame.getPlayer(0).getName()),str(currentGame.getCurrentSong()))
        
            index=1
            for i in top_scores:
                bottom_part = self.font.render(str(index)+") "+str(highScores.top_song_scores[str(currentGame.getCurrentSong())][i])+" : "+str(i), True, (0, 0, 0))
                bottom_part = self.transformImage(bottom_part)
                self.__screen.blit(bottom_part, (self.__margin_x,self.screen_y/4+self.font.get_linesize()*index))
                index+=1
            
            index=1
            if(str(currentGame.getPlayer(0).getName())!="New player"):
                for i in player_scores:
                    bottom_part = self.font.render(str(index)+") "+str(highScores.players_top_scores[str(currentGame.getPlayer(0).getName())][str(currentGame.getCurrentSong())][i])+" : "+str(i), True, (0, 0, 0))
                    bottom_part = self.transformImage(bottom_part)
                    x,y = bottom_part.get_size()
                    self.__screen.blit(bottom_part, (self.screen_x-self.__margin_x-x,self.screen_y/4+self.font.get_linesize()*index))
                    index+=1
        
        
        endScreen=True
        cntrl=Controller()
        
        unSelected = (0,0,0)
        selectedColor = (255,0,0)
        
        doneColor = unSelected
        myScoreColor = unSelected
        scoreColor = unSelected
        print 'selected', self.__selected
        if self.__selected ==1:
            myScoreColor = selectedColor
        elif self.__selected ==0:
            scoreColor = selectedColor
        elif self.__selected ==2:
            doneColor = selectedColor
        
        if(str(currentGame.getPlayer(0).getName())!="New player"):
            listSongs = self.__font.render("List Song High Scores: ", True, scoreColor)
            listSongs = self.transformImage(listSongs)
            text_x, text_y = listSongs.get_size()
            self.__screen.blit(listSongs, ((screen_x - text_x)/2,self.screen_y-self.font.get_linesize()*3))
        
            listSongs = self.__font.render("List My High Scores: ", True, myScoreColor)
            listSongs = self.transformImage(listSongs)
            text_x, text_y = listSongs.get_size()
            self.__screen.blit(listSongs, ((screen_x - text_x)/2,self.screen_y-self.font.get_linesize()*2))
        
        listSongs = self.__font.render("Done", True, doneColor)
        listSongs = self.transformImage(listSongs)
        text_x, text_y = listSongs.get_size()
        self.__screen.blit(listSongs, ((screen_x - text_x)/2,self.screen_y-self.font.get_linesize()*1))
        
        pygame.display.flip()     
        while endScreen:
            doneColor = unSelected
            myScoreColor = unSelected
            scoreColor = unSelected
            if self.__selected ==2:
                 myScoreColor = selectedColor
            elif self.__selected ==1:
                scoreColor = selectedColor
            elif self.__selected ==0:
                doneColor = selectedColor
        
            if(str(currentGame.getPlayer(0).getName())!="New player"):
                listSongs = self.__font.render("List Song High Scores: ", True, scoreColor)
                listSongs = self.transformImage(listSongs)
                text_x, text_y = listSongs.get_size()
                self.__screen.blit(listSongs, ((screen_x - text_x)/2,self.screen_y-self.font.get_linesize()*3))
        
                listSongs = self.__font.render("List My High Scores: ", True, myScoreColor)
                listSongs = self.transformImage(listSongs)
                text_x, text_y = listSongs.get_size()
                self.__screen.blit(listSongs, ((screen_x - text_x)/2,self.screen_y-self.font.get_linesize()*2))
        
            listSongs = self.__font.render("Done", True, doneColor)
            listSongs = self.transformImage(listSongs)
            text_x, text_y = listSongs.get_size()
            self.__screen.blit(listSongs, ((screen_x - text_x)/2,self.screen_y-self.font.get_linesize()*1))
            soundEffects.update()
            for event in pygame.event.get():
                
                currentStep = cntrl.checkEvent(event,1)
                if currentStep !=None:
                    endScreen=self.__checkNavEvent(currentStep)
            pygame.display.flip()
            pygame.time.wait(2)
            

        
        
"""
  ScreenBorder draws the screen that players will see.
"""

"""
   Created 17 February by Trey Brumley. Draws basic 
"""

"""
   Border looks like this
        astericks are notes
   =========================================
   |  UP-LEFT         UP         UP-RIGHT  |
   |           ================            |
   |           |              |            |
   |    LEFT   |  MAIN SCREEN |   RIGHT    |
   |           |              |            |
   |           ================            |
   | DOWN-LEFT       DOWN       DOWN-RIGHT |
   =========================================
   | *     *    *    |*|     SCORE         |
   =========================================
"""

import pygame
from pygame.locals import *
from Controller import Controller
from LoginMenu import LoginMenu
from FileLocations import FileLocations
    

class ScreenBorder (object):
    
    def __init__(self, screen):
        """
           Set default values for font, menu items
        """
        
        self.__screen = screen
        self.__screen_size = screen.get_size()
        self.__danceFloorCounter = 0
        self.__danceFloorArray = []
        
        self.__loadImages()
        
        self.lastMoves=[]
             
        self.__selected = 0
        self.__font = pygame.font.SysFont("arial", 48)
        self.__font_color = (244, 123, 25)
        self.__font_height = self.__font.get_linesize()
        
        
    def __loadImages(self):
        """
            Loads images for arrows, resizes them for current screen dimensions.
        """
        fileLocs=FileLocations()
            #load the arrow files
        up_arrow_file = fileLocs.images+r"\up_arrow.png"
        down_arrow_file = fileLocs.images+r"\down_arrow.png"
        right_arrow_file = fileLocs.images+r"\right_arrow.png"
        left_arrow_file = fileLocs.images+r"\left_arrow.png"
        down_right_arrow_file = fileLocs.images+r"\down_right_arrow.png"
        up_right_arrow_file = fileLocs.images+r"\up_right_arrow.png"
        down_left_arrow_file = fileLocs.images+r"\down_left_arrow.png"
        up_left_arrow_file = fileLocs.images+r"\up_left_arrow.png"
        
        self.__up_arrow = pygame.image.load(up_arrow_file).convert_alpha()
        self.__up_arrow = self.transformImage(self.__up_arrow)
        self.__down_arrow = pygame.image.load(down_arrow_file).convert_alpha()
        self.__down_arrow = self.transformImage(self.__down_arrow)
        self.__left_arrow = pygame.image.load(left_arrow_file).convert_alpha()
        self.__left_arrow = self.transformImage(self.__left_arrow)
        self.__right_arrow = pygame.image.load(right_arrow_file).convert_alpha()
        self.__right_arrow = self.transformImage(self.__right_arrow)
        self.__up_right_arrow = pygame.image.load(up_right_arrow_file).convert_alpha()
        self.__up_right_arrow = self.transformImage(self.__up_right_arrow )
        self.__up_left_arrow = pygame.image.load(up_left_arrow_file).convert_alpha()
        self.__up_left_arrow = self.transformImage(self.__up_left_arrow)
        self.__down_left_arrow = pygame.image.load(down_left_arrow_file).convert_alpha()
        self.__down_left_arrow = self.transformImage(self.__down_left_arrow)
        self.__down_right_arrow = pygame.image.load(down_right_arrow_file).convert_alpha()
        self.__down_right_arrow = self.transformImage(self.__down_right_arrow)
        
            #load person pic files
        man1_file = fileLocs.images+r"\chibi-girl.png"
        self.__man1 = pygame.image.load(man1_file).convert_alpha()
        self.__man1 = self.transformImage(self.__man1)
        miss_file = fileLocs.images+r"\miss.png"
        self.__miss = pygame.image.load(miss_file).convert_alpha()
        self.__miss = self.transformImage(self.__miss)
        girl_up_left = fileLocs.images+r"\girl_up_left.png"
        self.__girlUL = pygame.image.load(girl_up_left).convert_alpha()
        self.__girlUL = self.transformImage(self.__girlUL)
        girl_up_right = fileLocs.images+r"\girl_up_right.png"
        self.__girlUR = pygame.image.load(girl_up_right).convert_alpha()
        self.__girlUR = self.transformImage(self.__girlUR)
        self.__girlR = pygame.image.load(fileLocs.images+r"\girl_right.png").convert_alpha()
        self.__girlR = self.transformImage(self.__girlR)
        self.__girlL = pygame.image.load(fileLocs.images+r"\girl_left.png").convert_alpha()
        self.__girlL = self.transformImage(self.__girlL)
        self.__girlBL = pygame.image.load(fileLocs.images+r"\girl_back_left.png").convert_alpha()
        self.__girlBL = self.transformImage(self.__girlBL)
        self.__girlBR = pygame.image.load(fileLocs.images+r"\girl_back_right.png").convert_alpha()
        self.__girlBR = self.transformImage(self.__girlBR )
        
        
            #load hit button files
        hit_file = fileLocs.images+r"\hit.png"
        self.__hit = pygame.image.load(hit_file).convert_alpha()
        self.__hit = self.transformImage(self.__hit)
        
        #load the background
        background_file = fileLocs.images+r"\background.png"
        self.__background = pygame.image.load(background_file).convert_alpha()
        self.__background = self.transformImage(self.__background )
       
        self.__danceFloor = pygame.image.load(fileLocs.images+r"\dance_floor.png").convert_alpha()
        self.__danceFloor  = self.transformImage(self.__danceFloor)
        self.__danceFloor1 = pygame.image.load(fileLocs.images+r"\dance_floor1.png").convert_alpha()
        self.__danceFloor1 = self.transformImage(self.__danceFloor1)
        self.__danceFloor2 = pygame.image.load(fileLocs.images+r"\dance_floor2.png").convert_alpha()
        self.__danceFloor2 = self.transformImage(self.__danceFloor2)
        self.__danceFloor3 = pygame.image.load(fileLocs.images+r"\dance_floor3.png").convert_alpha()
        self.__danceFloor3 = self.transformImage(self.__danceFloor3)
        self.__danceFloor4 = pygame.image.load(fileLocs.images+r"\dance_floor4.png").convert_alpha()
        self.__danceFloor4 = self.transformImage(self.__danceFloor4)
        self.__danceFloor5 = pygame.image.load(fileLocs.images+r"\dance_floor5.png").convert_alpha()
        self.__danceFloor5 = self.transformImage(self.__danceFloor5)
        self.__danceFloor6 = pygame.image.load(fileLocs.images+r"\dance_floor6.png").convert_alpha()
        self.__danceFloor6 = self.transformImage(self.__danceFloor6)
        self.__danceFloor7 = pygame.image.load(fileLocs.images+r"\dance_floor7.png").convert_alpha()
        self.__danceFloor7 = self.transformImage(self.__danceFloor7)
        self.__danceFloor8 = pygame.image.load(fileLocs.images+r"\dance_floor8.png").convert_alpha()
        self.__danceFloor8 = self.transformImage(self.__danceFloor8)
        self.__danceFloor9 = pygame.image.load(fileLocs.images+r"\dance_floor9.png").convert_alpha()
        self.__danceFloor9 = self.transformImage(self.__danceFloor9)
        self.__danceFloor10 = pygame.image.load(fileLocs.images+r"\dance_floor10.png").convert_alpha()
        self.__danceFloor10 = self.transformImage(self.__danceFloor10)
        self.__danceFloor11 = pygame.image.load(fileLocs.images+r"\dance_floor11.png").convert_alpha()
        self.__danceFloor11 = self.transformImage(self.__danceFloor11)
        
        self.__danceFloorArray = [self.__danceFloor,self.__danceFloor1, self.__danceFloor2, self.__danceFloor3, self.__danceFloor4,\
                                  self.__danceFloor5, self.__danceFloor6, self.__danceFloor7, self.__danceFloor8, self.__danceFloor9, \
                                  self.__danceFloor10, self.__danceFloor11]
        
        
        self.__offset_x = 80
        self.__offset_y = 75
        self.__menuItem_height = 100
        self.__menu_Y_bump = 10
          #must eventually allow for different sized screens
        self.screen_x, self.screen_y = self.__screen_size
        
    def DrawBackground(self):
        """
            Draws the background of the single player mode. 
        """
        self.__screen.fill((255, 255, 255))
        
        #display background
        x,y = self.__danceFloorArray[self.__danceFloorCounter].get_size()
        self.__screen.blit(self.__danceFloorArray[self.__danceFloorCounter], (0,self.screen_y-y))
        
        self.__screen.blit(self.__background, (0,0))
        
        
            #display diagonal arrows
        self.image_x, self.image_y = self.__up_left_arrow.get_size()
        
        self.__screen.blit(self.__up_left_arrow, (0 ,0))
        self.image_x, self.image_y = self.__up_right_arrow.get_size()
        self.__screen.blit(self.__up_right_arrow, (self.screen_x - self.image_x ,0))
        self.image_x, self.image_y = self.__down_left_arrow.get_size()
        self.__screen.blit(self.__down_left_arrow, (0 ,self.screen_y-self.image_y - self.__font_height))
        self.image_x, self.image_y = self.__down_right_arrow.get_size()
        self.__screen.blit(self.__down_right_arrow, (self.screen_x - self.image_x ,self.screen_y - self.image_y - self.__font_height))
        
            #display cardinal arrows
        self.image_x, self.image_y = self.__up_arrow.get_size()
        self.__screen.blit(self.__up_arrow, (self.screen_x/2 -self.image_x/2 ,0))
        self.image_x, self.image_y = self.__right_arrow.get_size()
        self.__screen.blit(self.__right_arrow, (self.screen_x - self.image_x ,((self.screen_y-self.__font_height)/2)-self.image_y/2))
        self.image_x, self.image_y = self.__left_arrow.get_size()
        self.__screen.blit(self.__left_arrow, (0 ,((self.screen_y-self.__font_height)/2)-self.image_y/2 ))
        self.image_x, self.image_y = self.__down_arrow.get_size()
        self.__screen.blit(self.__down_arrow, (self.screen_x/2 -self.image_x/2,self.screen_y - self.image_y - self.__font_height))
        
        
    def DrawMainBox(self, moves):
        """
            Draws the main box which includes the character's dance moves
        """
        screen_x, screen_y = self.__screen_size
        
            
        if(len(moves)!=0):
            atStep=moves[len(moves)-1]
            if(atStep.getLocation()==(0,0)):
                self.image_x, self.image_y = self.__girlBL.get_size()
                self.__screen.blit(self.__girlBL, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(0,1)):
                self.image_x, self.image_y = self.__girlL.get_size()
                self.__screen.blit(self.__girlL, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(0,2)):
                self.image_x, self.image_y = self.__girlUL.get_size()
                self.__screen.blit(self.__girlUL, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(1,0)):
                self.image_x, self.image_y = self.__man1.get_size()
                self.__screen.blit(self.__man1, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(1,2)):
                self.image_x, self.image_y = self.__man1.get_size()
                self.__screen.blit(self.__man1, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(2,0)):
                self.image_x, self.image_y = self.__girlBR.get_size()
                self.__screen.blit(self.__girlBR, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(2,1)):
                self.image_x, self.image_y = self.__girlR.get_size()
                self.__screen.blit(self.__girlR, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
            elif(atStep.getLocation()==(2,2)):
                self.image_x, self.image_y = self.__girlUR.get_size()
                self.__screen.blit(self.__girlUR, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2))
            else:
                self.image_x, self.image_y = self.__miss.get_size()
                self.__screen.blit(self.__miss, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 
        else:
            self.image_x, self.image_y = self.__miss.get_size()
            self.__screen.blit(self.__miss, (self.screen_x/2 -self.image_x/2 ,((self.screen_y-self.__font_height)/2)-self.image_y/2)) 

    def DrawHitBoxes(self, moves):
        """
            Draws which step the player has just hit
        
        """
        if(len(moves)!=0):
            atStep=moves[len(moves)-1]
            #display diagonal arrows hit
            if(atStep.getLocation()==(0,2)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (2 ,self.__font_height))
            elif(atStep.getLocation()==(2,2)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (self.screen_x - self.image_x ,self.__font_height))
            elif(atStep.getLocation()==(0,0)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (0 ,self.screen_y-self.image_y))
            elif(atStep.getLocation()==(2,0)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (self.screen_x - self.image_x ,self.screen_y - self.image_y))
            elif(atStep.getLocation()==(1,2)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (self.screen_x/2 -self.image_x/2 ,self.__font_height))
            elif(atStep.getLocation()==(2,1)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (self.screen_x - self.image_x ,((self.screen_y+self.__font_height)/2)-self.image_y/2))
            elif(atStep.getLocation()==(0,1)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (0 ,((self.screen_y+self.__font_height)/2)-self.image_y/2 ))
            elif(atStep.getLocation()==(1,0)):
                self.image_x, self.image_y = self.__hit.get_size()
                self.__screen.blit(self.__hit, (self.screen_x/2 -self.image_x/2,self.screen_y - self.image_y))
       
    def drawScreen(self, moves,screenInf,pointsPerHit,totalPoints,currentGame):
        """
           Draws visual elements to screen.  draws all arrows (and HIT pictures to indicate which arrow has been pressed)
           Also allows for the 
        """       

        self.DrawBackground()

        self.DrawMainBox(moves)
        self.DrawHitBoxes(moves)
        
        self.__screen.blit(screenInf.font.render((str(currentGame)), True, (0, 0, 0)),(self.screen_x - 350,0))
        self.__screen.blit(screenInf.font.render("Points: "+str(int(totalPoints))+"   Points for Current Step: "+str(int(pointsPerHit)), True, (0, 0, 0)),(0,0))
        pygame.display.flip()
        
    def IncrementDanceFloorCounter(self):
        if self.__danceFloorCounter < (len(self.__danceFloorArray) - 1):
            self.__danceFloorCounter += 1
        else:
            self.__danceFloorCounter = 0
            
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
        
        
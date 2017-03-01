"""
   GameController main game loop that ties in navigation and gamew
"""

"""
   GameController started 12 Feb by Trey Brumley -- created a main loop as well as an initialization method
   29 March -- added fullscreen support JCisarano
"""

HIT_TOL = 0.200
BEAT_TOL = 0.033

DoClap = False
global gameOn
gameOn=True

import sys
import os
sys.path.append("..")
mydir = os.path.dirname(sys.argv[0])
print mydir,'test'
import pygame
import thread
from pygame.locals import *
from bisect import bisect

from FileLocations import FileLocations
from Controller import Controller
from GameInfo import GameInfo

from IntroMenu import IntroMenu
from SplashMenu import SplashMenu
from SongChooserMenu import SongChooserMenu
from SoundEffectController import SoundEffectController
from GameOverScreen import GameOverScreen
import SinglePlayerMode
import CareerMode

mydir = os.path.dirname(sys.argv[0])
print sys.argv, 'test'
if mydir:
        os.chdir(mydir)

music = pygame.mixer.music
class screenInfo():
    pygame.init()
    game = GameInfo()
    SCREEN_SIZE = game.getSettings().getScreenSize()
    font = pygame.font.SysFont("arial", 16);
    font_height = font.get_linesize()

def startMenu():
    """
        This is the main method of the game. Initilizes main variables, and passes control to the splash menu
    """
    
    screenInf=screenInfo()
    pygame.init()
    screen = pygame.display.set_mode(screenInf.SCREEN_SIZE, FULLSCREEN, 32)
    pygame.mouse.set_visible(False)
    splash = SplashMenu(screen)
    menu = IntroMenu(screen) #####Create IntroMenu objectu
    
    running=True
    
    splash.drawSplashMenu()  ####Splash only drawn once at beginning of game
    
    while running:
            menu.drawIntroMenu(screen)  ####Draws menu to screen, controls game during this time
            currentGame = menu.getGameInfo()
            if(currentGame == None):
                exit()

    
startMenu()
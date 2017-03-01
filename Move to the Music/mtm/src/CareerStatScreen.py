"""
CareerStatScreen will show/tell the player
how they did on a certain song.  It will offer
the option to replay the song again or
go back to the CareerOpenScreen to select another song.
This is where the criteria for CareerMode will come into
play.  With certain requirements put into place, CareerStatScreen
will show or tell the player if they achieved the criteria or not.
If they did, it will pass a congrats to CareerOpenScreen and possibly
unlock the next group, however if not the next group or level will 
not unlock.
"""

"""
CareerStatScreen started on 21 March 2008 by Zach Swartz
updated on 26 March 2008 by Zach Swartz
"""

import pygame, os, sys
pygame.init()

def start(gameInfo):
    
    
    screen = pygame.display.set_mode((500,400))
    
    font = pygame.font.SysFont("arial", 20, False, False)
    stat = font.render("Dancin' Stats", True, (0,0,255))
    stat2 = font.render("Total Points  -",True, (255,255,255))
    stat3 = font.render("Combo's Hit   -", True, (255,255,255))
    stat4 = font.render("Accuracy      - ", True, (255,255,255))
        
    stat5 = font.render("Replay Song", True, (0, 0, 255))
    stat6 = font.render("Done", True, (0,0,255))
    
    screen.blit(stat, (50,50))
    screen.blit(stat2, (80, 80))
    screen.blit(stat3, (80, 100))
    screen.blit(stat4, (80, 120))
    screen.blit(stat5, (50, 180))
    screen.blit(stat6, (50, 220))
    
    pygame.display.flip()
    
    unlockSong = 0
    if (gameInfo.getCurrentScore() >=10000 and gameInfo.getCombosHit >=3):
        unlockSong = unlockSong + 1
    
    endScreen = True
    while endScreen == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN: 
                endScreen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                import CareerOpenScreen
                CareerOpenScreen.careerOpenScreen(unlockSong)
                 
                
    pygame.time.wait(2)
    
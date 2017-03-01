import pygame, sys, os
from pygame.locals import *

dir(pygame)

pygame.init()
pygame.mixer.init()

#File for certain song - where one.mp3.mp3 is can add any song you want
filename = "D:\My Documents\School Work\Comp 523\Projects\MediaPlayer\MediaPlayer\src\MediaPlayer\Music\one.mp3.mp3"

window = pygame.display.set_mode((468, 468))

pygame.display.set_caption('Media Player')

def input(events): 
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: 
            sys.exit(0) 
        elif event.type == KEYDOWN and event.key == K_RETURN:
            
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
        elif event.type == KEYDOWN and event.key == K_PAUSE:
            pygame.mixer.music.pause()
            
        elif event.type == KEYDOWN and event.key == K_TAB:
            pygame.mixer.music.unpause()
            
             
while True: 
    input(pygame.event.get()) 



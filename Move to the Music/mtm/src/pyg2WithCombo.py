HIT_TOL = 0.200
BEAT_TOL = 0.033

totalPoints=0
pointsPerhit=0

DoClap = False

import sys
import os
import pygame


#my own import statement
from Combo import combo
from utils.FileLocations import FileLocations

fileLocs=FileLocations()
pygame.mixer.pre_init(44100,-16,2,1024*2)
pygame.init()



music = pygame.mixer.music
from bisect import bisect

pygame.mixer.pre_init(44100, -16, 2, 1024*2)
pygame.init()

songfile = fileLocs.songs+r'\BillyJean.wav'
timefile = fileLocs.beats+r'\BillyJean.times'

music.load(songfile)
print fileLocs.soundeffects+r'\clap.wav'





#my own constants
MAXSTEPS = 5
playerSteps = []
    
comboA = combo("(0,0), (0,0), (0,0), (0,0)")

comboDictionary= [comboA]

#end of my constants







times = [ float(t.strip()) for t in file(timefile, 'rt') ]
def GetDelta(t):
    n = bisect(times, t)
    d1 = t - times[n-1]
    d2 = times[n] - t
    if d1 < d2:
        return -d1
    else:
        return d2

size = width, height = 320, 240
origin = height/2
scale = height/2
bar_w = 16
bar_n = width/bar_w

screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except pygame.error:
    pass

music.play()

errors = []

run = True
while run:
    t = music.get_pos() * 0.001
    dt = GetDelta(t)
    hit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            f = max(-1, min(1, (dt / HIT_TOL)))
            
            
            
            hit = abs(f) < 0.5
            
            
            #my own code
            if hit:
                playerSteps.append(event.key) 
                print playerSteps
            else:
                print "you missed the beat"
            if len(playerSteps) > MAXSTEPS: 
                playerSteps.pop(0)
            
           
            
            for item in comboDictionary:
                if playerSteps[MAXSTEPS - 3:MAXSTEPS] == item.getComboList():
                    print "you did a 3 button combo"
                #if they did a combo, reset the playerSteps list
                    break
                if playerSteps[MAXSTEPS - 4:MAXSTEPS] == item.getComboList():
                    print "you did a 4 button combo"
                    break
                if playerSteps[MAXSTEPS - 5:MAXSTEPS] == item.getComboList():
                    print "you did a 5 button combo"
                     
            
            #end of my code
            
            
            
            
            errors.append(f)
        if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            f = max(-1, min(1, (dt / HIT_TOL)))
            hit = abs(f) < 0.5
            errors.append(f)
        else:
        pygame.time.wait(2)

    if hit and DoClap:
        c = clap.play()
        #c.Volume = (1 - abs(f)) * 100
        pass

    if abs(dt) < BEAT_TOL:
        screen.fill((255, 255, 255))
    else:
        screen.fill((0, 0, 0))
    for i, f in enumerate(errors[-bar_n:]):
        x1 = i*bar_w
        w = bar_w
        if f < 0:
            y1 = origin + f * scale
        else:
            y1 = origin
        h = abs(f) * scale
        if f < 0:
            c = (255, 0, 0)
        else:
            c = (0, 255, 0)
        screen.fill(c, pygame.Rect(x1, y1, w, h))
    pygame.display.flip()

print 'exiting'

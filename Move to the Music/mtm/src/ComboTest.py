"""
   SinglePlayerMode loads a predetermined song, plays it and detects events from the user!!!!
"""

"""
   SinglePlayerMode refactored March 19 2:00 am
"""

from Controller import Controller
from Score import Score
from GoodStep import GoodStep
from Combo import combo
from FileLocations import FileLocations
from bisect import bisect
import sys
import os
import pygame

def startGame(screen,screenInf,currentGame):
    HIT_TOL = 0.200
    BEAT_TOL = 0.033
    MAXSTEPS = 5
    
    global totalPoints
    totalPoints = 0
    pointsPerHit=0
    goodSteps=[]
    
    #temporary creation of dictionary
    goodstepA =GoodStep(6)
    goodstepB = GoodStep(1)
    comboA = combo((goodstepA, goodstepA, goodstepA, goodstepA))
    comboB = combo((goodstepB, goodstepB, goodstepB))
    comboDictionary= [comboA,comboB]
    #end temporary 
    
    fileLocs=FileLocations()
    scorer=Score()
   
    songfile = fileLocs.songs+r"\BillyJean.wav"
    timefile = fileLocs.beats+r"\BillyJean.times"
    
    #initialize pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024*2)
    pygame.init()
    music = pygame.mixer.music
    music.load(songfile)
    
    #get the times from the times file
    times = [ float(t.strip()) for t in file(timefile, 'rt') ]
    
    
    #FUNCTIONS FOR SINGLEPLAYER
    
    #get the change in time between the beat times and the current time
    def GetDelta(t):
        n = bisect(times, t)
        d1 = t - times[n-1]
        d2 = times[n] - t
        if d1 < d2:
            return -d1
        else:
            return d2
    
    #figure out if the change in time / tolerance is < .5, it if is, it's a hit
    def isWithinTolerance(changeInTime, hitTolerance):
        dt = changeInTime
        ht = hitTolerance
        
        f = max(-1, min(1, (dt / ht)))
        hit = abs(f) < 0.5
        errors.append(f)
        return hit
    
    #compare containers of goodsteps and see if they are equal
    def CompareGoodStepContainers(container1, container2):
        isTrue = True
        if len(container1) != len(container2):
            return False
        for i in range(0, len(container1)):
            if container1[i].getLocation() != container2[i].getLocation():
                return False
        return isTrue
            
        
    
    #combo Detection will return combo if yes, none if not
    def CheckForCombo():
        for item in comboDictionary:
            if CompareGoodStepContainers(goodSteps[MAXSTEPS - 3:MAXSTEPS],item.getComboList()):
                print "you did a 3 button combo"
            #if they did a combo, reset the playerSteps list
                break
            if CompareGoodStepContainers(goodSteps[MAXSTEPS - 4:MAXSTEPS],item.getComboList()):
                print "you did a 4 button combo"
                break
            if CompareGoodStepContainers(goodSteps[MAXSTEPS - 5:MAXSTEPS],item.getComboList()):
                print "you did a 5 button combo"           
    
    
    
    def DrawNoteBars():
        origin = screen.get_height()/2
        scale = screen.get_height()/2
        bar_w = 16
        bar_n = screen.get_width()/bar_w
        
        for i, f in enumerate(errors[-bar_n:]):
            x1 = i*bar_w
            w = bar_w
            if f < 0:
                y1 = origin + f * scale
            else:
                y1 = origin
            h = abs(f) * scale
            if abs(f) < .05:
                c = (255, 0, 255)
            elif abs(f)<.15:
                c = (0, 255, 0)
            elif abs(f)<.25:
                c=(0,0,255)
            else:
                c=(255,0,0)
            screen.fill(c, pygame.Rect(x1, y1, w, h))
            
            
    def PrepareScreen():
        if abs(dt) < BEAT_TOL:
            screen.fill((255, 255, 255))
        else:
            screen.fill((0, 0, 0))
                  
    def UpdateScreen():
        screen.blit(screenInf.font.render((str(currentGame)), True, (255, 255, 255)),(0,0))
        screen.blit(screenInf.font.render("Points: "+str(int(totalPoints))+"   Points for Current Step: "+str(int(pointsPerHit)), True, (255, 255, 255)),(0,screenInf.font.get_linesize()))
        pygame.display.flip()
        
    def ScorePoints():  
        ScoreHit()
       # ScoreCombo()
          
    def ScoreHit():
        pointsPerHit=scorer.scoreHit(goodSteps,dt)
        pointsPerHit=int(pointsPerHit)
        global totalPoints 
        totalPoints += pointsPerHit
        
    def ScoreCombo():
        k=1 #this does nothing right now, just a placeholder"
        
        
    
    #start the single player mode and initialize
    music.play()
    errors = []
    cntrl=Controller()
    
    run = True
    #start the game loop
    while run:
        #get current time position in song
        t = music.get_pos() * 0.001
        dt = GetDelta(t)
        
        for event in pygame.event.get():
            #see if it's a goodStep
            currentStep = cntrl.checkEvent(event,t)
            if currentStep != None: 
            
            #check to see if you hit the beat
                if isWithinTolerance(dt, HIT_TOL) == True:
                    goodSteps.append(currentStep)
                
                    #see if goodSteps is greater than the maximum # you want to keep track of, if it is, pop the stack    
                    if len(goodSteps) > MAXSTEPS: 
                        goodSteps.pop(0)
                    
                    #check to see if a combo
                    CheckForCombo()
                    
                    #score hit and combo here
                    ScorePoints()    
                
        else:
            pygame.time.wait(2)
            pass

        PrepareScreen()
        DrawNoteBars()
        UpdateScreen()
        
    print "exiting"
    return round(totalPoints)

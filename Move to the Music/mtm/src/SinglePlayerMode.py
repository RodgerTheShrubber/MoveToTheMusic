"""
   SinglePlayerMode loads a predetermined song, plays it and detects events from the user!!!!
"""

"""
   SinglePlayerMode refactored March 19 2:00 am
"""

from Controller import Controller
from GoodStep import GoodStep
from FileLocations import FileLocations
from ScreenBorder import ScreenBorder
from GameInfo import GameInfo
from SoundEffectController import SoundEffectController
from ComboDictionary import ComboDictionary
from Combo import Combo
from Score import Score
from bisect import bisect
from Player import Player
import CareerStatScreen
import sys
import os
import thread
import pygame

#takes a screen, screen information, and gameInfo
def startGame(screen,screenInf,currentGame):
    """
        Starts the game. This method grabs control of the game, detects beats, scores the beats and returns 
        the score of the game when the song is finished
    """
    HIT_TOL = 0.300
    BEAT_TOL = 0.033
    
    gameInfo = currentGame
    player = gameInfo.getPlayer(0)
    gameStats = player.getGameStats()
    gameStats.newRound()
    
    difficulty = player.getProfile().getDifficulty()
    if (difficulty ==0):
        FAIR_DIFF = .3
    
    if (difficulty ==1):
        FAIR_DIFF = .25
    
    if (difficulty ==2):
        FAIR_DIFF = .2
            
            
    HIT_TOL = FAIR_DIFF
    BEAT_TOL = 0.033
    
    comboDictionary = ComboDictionary()
    fileLocs=FileLocations()
    scorer=Score()
    screenBorder=ScreenBorder(screen)
    

    
    
    
    
    
    
   
    #songfile = fileLocs.songs+r"\CodeMonkey.mp3"
    #timefile = fileLocs.beats+r"\CodeMonkey.times"
    
    songfile =""
    songfile = fileLocs.songs+ gameInfo.getCurrentSong()[1] +".ogg"
    timefile = fileLocs.beats+ gameInfo.getCurrentSong()[1] +".times"
    
    
    #initialize pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024*2)
    pygame.init()
    music = pygame.mixer.music
    try:
        music.load(songfile)
    except:
        try:
            songfile = fileLocs.songslist+ gameInfo.getCurrentSong()[1] +".mp3"
            music.load(songfile)
        except:
            songfile = fileLocs.songs+ gameInfo.getCurrentSong()[1] +".mp3"
            music.load(songfile)
    
    music.set_volume(gameInfo.getSettings().getMusicVolume()/100.0)
    

    
    #initialize sound controller

    soundController = SoundEffectController(gameInfo.getSettings().getVoiceVolume()/ 100.0)
    
    
    #get the times from the times file
    times = [ float(t.strip()) for t in file(timefile, 'rt') ]
    
    
    #FUNCTIONS FOR SINGLEPLAYER
    
    #get the change in time between the beat times and the current time
    def GetDelta(t):
        n = bisect(times, t)
        d1 = t - times[n-1]
        try:
            d2 = times[n] - t
        except IndexError:
            return (0,False)
        if d1 < d2:
            return (-d1,True)
        else:
            return (d2, True)
        
        
    
    #figure out if the change in time / tolerance is < .5, it if is, it's a hit
    def HitOnBeat(changeInTime, hitTolerance):
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
        currentStepLength = len(gameStats.getComboSteps())
        comboStepList = gameStats.getComboSteps()
        for item in comboDictionary.getCombosOfSize(3):
            if CompareGoodStepContainers(comboStepList[currentStepLength - 3:currentStepLength],item.getSteps()):  
                return item
        for item in comboDictionary.getCombosOfSize(4):
            if CompareGoodStepContainers(comboStepList[currentStepLength - 4:currentStepLength],item.getSteps()):   
                return item
        for item in comboDictionary.getCombosOfSize(5):    
            if CompareGoodStepContainers(comboStepList[currentStepLength - 5:currentStepLength],item.getSteps()):
                return item
        return None      
        
    
    #prepare screen flash        
    def FlashOrUpdateScreen(gameStats):
        if abs(dt) < BEAT_TOL:
            #screen.fill((0, 0, 0))
            screenBorder.IncrementDanceFloorCounter()
            #pygame.display.flip()
       
        screenBorder.drawScreen(gameStats.getGoodSteps(),screenInf,gameStats.getPointsPerHit(),gameStats.getCurrentScore(),gameInfo.getGameMode())
    
    
    #update score   
    def UpdateScore(dt):
        
        
        #set points per hit
        gameStats.setPointsPerHit(int(scorer.scoreHit(gameStats.getGoodSteps(),difficulty, dt, gameStats.getCurrentCombo())))
    
        currentScore = gameStats.getCurrentScore()
        
        pointsForCurrentHit = gameStats.getPointsPerHit()
        currentScore += pointsForCurrentHit
        
        gameStats.setCurrentScore(currentScore)
    
        
    def checkPositiveSounds():
        playPointsSound()
        pass
        

    #plays number of points based on how many points there are, every 100,000
    def playPointsSound():
        totalScore = gameStats.getCurrentScore()
        pointGoal = gameStats.getPointGoal()
        if totalScore >= pointGoal:
            roundScore = totalScore
            i = 10
            while roundScore/i > 10:
                i *= 10
            soundController.playNumberSound(roundScore/i *i)
            gameStats.setPointGoal(pointGoal + 100000)
    
        
            
            
    def comboProcessing():
        gameStats.setCurrentCombo(CheckForCombo())
        if (gameStats.getCurrentCombo() != None):
            soundController.playComboInSong(gameStats.getCurrentCombo())
            gameStats.clearComboSteps()
            
    def stepProcessing(currentStep):
        gameStats.addStep(currentStep)
        gameStats.setBeatsHit(gameStats.getBeatsHit() + 1)
        gameStats.setBeatsAttempted(gameStats.getBeatsAttempted() + 1)
        soundController.playHitSound()     
            
    def missedBeat():
        #soundController.playMissSound()
        gameStats.setBeatsAttempted(gameStats.getBeatsAttempted() + 1)
        gameStats.clearGoodSteps()
        gameStats.clearComboSteps()
    
    #start the single player mode and initialize
    
    music.play()
    errors = []
    cntrl=Controller()
    cntrl2 = Controller(2)
    
    run = True
    #start the game loop
    while run:
        #get current time position in song
        t = music.get_pos() * 0.001
        dt,run = GetDelta(t)
        
        for event in pygame.event.get():
            #check for escape
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    music.stop()
                    run = False
                    
                    
            #you could do for each controller, check if current step is a goodstep, then do the stuff
            #see if it's a goodStep
            currentStep = cntrl.checkEvent(event,t)
            currentStepPlayer2 = cntrl2.checkEvent(event,t)
            if currentStep != None: 
            #check to see if you hit the beat
                #if you hit the beat
                if HitOnBeat(dt, HIT_TOL) == True:
                    stepProcessing(currentStep)
                    comboProcessing()
                              
                    #update the score
                    UpdateScore(dt)
                    checkPositiveSounds()
                    
                else:
                    #clear the goodSteps and combo list, because you stepped on a wrong beat
                    missedBeat()
            elif currentStepPlayer2 != None: 
            #check to see if player 2 hit the beat
            #if you hit the beat
                if HitOnBeat(dt, HIT_TOL) == True:
                    stepProcessing(currentStepPlayer2)
                    comboProcessing()
                              
                    #update the score
                    UpdateScore(dt)
                    checkPositiveSounds()
                else:
                    #clear the goodSteps and combo list, because you stepped on a wrong beat
                    missedBeat()
            
                    
                
        else:
            pygame.time.wait(2)
        
        FlashOrUpdateScreen(gameStats)
        soundController.update()
        gameStats.setCurrentCombo(None)
        
    gameInfo.getPlayer(0).setGameStats(gameStats)
    return gameInfo

"""
   CareerMode loads a song from a passed in variable.
   CareerMode will play the song and keep track of
   vital stats towards a players success of failure 
   of the game.  It will be keeping track of
   Notes Attempted, Notes Hit, Combo's Hit, and Points.
"""

"""
   CareerMode restarted 24 March 2008 by Zach Swartz
   Updated 26 March 2008 by Zach Swartz
"""

"""
- method which figure out when to say combos
- method which figures out if user gets combos
- method which gives feedback depending on if they did combo
- keeping track of all stats (beats hit, beats attempted, points)
"""

"""in the middle of fixing"""

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
import CareerStatScreen
import random
import sys
import os
import thread
import pygame
#takes a screen, screen information, and gameInfo
def startGame(screen,screenInf,currentGame):
     
    gameInfo = currentGame
    player = gameInfo.getPlayer(0)
    gameStats = player.getGameStats()
    gameStats.newRound()
    
    difficulty = player.getProfile().getDifficulty()
    if (difficulty ==0):
        FAIR_DIFF = .3
        combosNeeded = 5
    
    if (difficulty ==1):
        FAIR_DIFF = .25
        combosNeeded = 10
    
    if (difficulty ==2):
        FAIR_DIFF = .2
        combosNeeded = 15
            
            
    HIT_TOL = FAIR_DIFF
    BEAT_TOL = 0.033
    
    comboDictionary = ComboDictionary()
    fileLocs=FileLocations()
    scorer=Score()
    screenBorder=ScreenBorder(screen)
   
    songfile = fileLocs.songs+ gameInfo.getCurrentSong()[1] +".ogg"
    timefile = fileLocs.beats+ gameInfo.getCurrentSong()[1] +".times"
    
    #initialize pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024*2)
    pygame.init()
    music = pygame.mixer.music
    music.load(songfile)
    music.set_volume(gameInfo.getSettings().getMusicVolume()/100.0)

    
    #initialize sound controller
    soundController = SoundEffectController(gameInfo.getSettings().getVoiceVolume()/ 100.0)
    clock = pygame.time.Clock()
    
    
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
            return None
        if d1 < d2:
            return -d1
        else:
            return d2
    
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
        gameStats.setPointsPerHit(int(scorer.scoreHit(gameStats.getGoodSteps(),difficulty,dt, gameStats.getCurrentCombo())))
        
        
        currentScore = gameStats.getCurrentScore()
        
        pointsForCurrentHit = gameStats.getPointsPerHit()
        currentScore += pointsForCurrentHit
        
        gameStats.setCurrentScore(currentScore)
    
        
    def checkPositiveSounds():
        playPointsSound()
        

    #plays number of points based on how many points there are, every 100,000
    def playPointsSound():
        totalScore = gameStats.getCurrentScore()
        pointGoal = gameStats.getPointGoal()
        if totalScore >= pointGoal:
            soundController.playNumberSound(totalScore)
            print "you've reached " + str(pointGoal) + " points!"
            gameStats.setPointGoal(pointGoal + 100000)
    
    #depending on the level, create a list of combos to ask for        
    def createAskComboList():
        #easy
        comboListtoAsk = []
            
        currentLevel = gameInfo.getCurrentLevel()
        #currentLevel = 9
        print "current level is " + str(currentLevel)
        
        if currentLevel ==1: 
            combos= comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
            comboListtoAsk = combos + combos1
        
        elif currentLevel ==2:
            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
            comboListtoAsk = combos + combos1 + combos2
            
        elif currentLevel ==3:
            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
            combos3 = comboDictionary.getCombosOfSizeAndDifficulty(4, "easy")
            comboListtoAsk = combos + combos1 + combos2 + combos3

            
        elif currentLevel ==4:
            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
            combos3 = comboDictionary.getCombosOfSizeAndDifficulty(4, "easy")
            combos4 = comboDictionary.getCombosOfSizeAndDifficulty(4, "medium")
            combos5 = comboDictionary.getCombosOfSizeAndDifficulty(4, "hard")
            combos6 = comboDictionary.getCombosOfSizeAndDifficulty(5, "easy")
            comboListtoAsk = combos + combos1 + combos2 + combos3 + combos4 + combos5 + combos6 
            
        elif currentLevel ==5:
            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
            combos3 = comboDictionary.getCombosOfSizeAndDifficulty(4, "easy")
            combos4 = comboDictionary.getCombosOfSizeAndDifficulty(4, "medium")
            combos5 = comboDictionary.getCombosOfSizeAndDifficulty(4, "hard")
            combos6 = comboDictionary.getCombosOfSizeAndDifficulty(5, "easy")
            combos7 = comboDictionary.getCombosOfSizeAndDifficulty(5, "medium")
            combos8 = comboDictionary.getCombosOfSizeAndDifficulty(5, "hard")
            comboListtoAsk = combos + combos1 + combos2 + combos3 + combos4 + combos5 + combos6 + combos7 + combos8
        
        
        
        gameStats.setAskedComboList(comboListtoAsk)
        

    def askForCombo():
        #get a combo to be played, randomly from askedComboList

        comboList = gameStats.getAskedComboList()
        gameStats.setAskedCombo(comboList[random.randrange(0,(len(comboList)))])
        combo = gameStats.getAskedCombo()
        
        soundController.queueSoundFile(fileLocs.careerSounds+ "\\tryCombo.ogg")
        playComboSteps(combo)
        
        
        print "Let's try doing a combo! " + combo.getName()
        print combo.getStepNameList()

        
    def playComboSteps(combo):   
        steps = combo.getSteps()
        for step in steps:
            soundController.queueSoundFile(step.getSoundFile())
                 
    def checkForAskedCombo():
        if gameStats.getCurrentCombo() == gameStats.getAskedCombo():
            print "Great Job, you hit the combo!"
            gameStats.setAskedCombosHit(gameStats.getAskedCombosHit() + 1)
            gameStats.setAskedCombo(None)
            
    def comboProcessing():
        gameStats.setCurrentCombo(CheckForCombo())
        if (gameStats.getCurrentCombo() != None):
            soundController.playComboInSong(gameStats.getCurrentCombo())
            checkForAskedCombo()
            gameStats.clearComboSteps()
            
    def stepProcessing(currentStep):
        gameStats.addStep(currentStep)
        gameStats.setBeatsHit(gameStats.getBeatsHit() + 1)
        gameStats.setBeatsAttempted(gameStats.getBeatsAttempted() + 1)
        soundController.playHitSound()     
            
    def missedBeat():
        soundController.playMissSound()
        gameStats.setBeatsAttempted(gameStats.getBeatsAttempted() + 1)
        gameStats.clearGoodSteps()
        gameStats.clearComboSteps()
                           
    
    #start the single player mode and initialize
    music.set_volume(.5)
    music.play()
    errors = []
    cntrl=Controller()
    createAskComboList()
    
    timeSinceCombo = 0
    timeOfCombo = 0
    repeatedCombo = False
    
    run = True
    #start the game loop
    while run:
        #get current time position in song
        t = music.get_pos() * 0.001
        dt = GetDelta(t)
        if  t > times[len(times) -1]:
            music.stop()
            run = False 
            break
        
        
        #here we're asking for a combo, and figuring out when it was asked
        #if you don't hit it in 10 seconds, we ask you for it again. after another 10, new combo
        timeSinceCombo = t - timeOfCombo 
        if gameStats.getAskedCombo() == None:
            askForCombo()
            timeOfCombo= t
            repeatedCombo = False
        elif (timeSinceCombo > 15):
            #ask for a new combo if you've already repeated it
            if repeatedCombo == True:
                askForCombo()
                repeatedCombo = False
            #say the same combo steps again
            else:
                playComboSteps(gameStats.getAskedCombo())
                repeatedCombo = True
            timeOfCombo = t
                
        
        for event in pygame.event.get():
            
            
            #check for escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    music.stop()
                    run = False
                    
            #see if it's a goodStep
            currentStep = cntrl.checkEvent(event,t)
            if currentStep != None: 
            #check to see if you hit the beat
                #if you hit the beat
                if HitOnBeat(dt, HIT_TOL) == True:
                    
                    stepProcessing(currentStep)
                    
                    #check to see if it was a combo
                    comboProcessing()
                             
                    #update the score
                    UpdateScore(dt)
                    checkPositiveSounds()
                    
                    
                else:
                    #clear the goodSteps and combo list, because you stepped on a wrong beat
                    missedBeat()
                
        else:
            pygame.time.wait(2)
            pass
        
        clock.tick(30)
        FlashOrUpdateScreen(gameStats)
        soundController.update()
        gameStats.setCurrentCombo(None)
        
    
    
    
        
    if (gameStats.getAskedCombosHit() >= combosNeeded):
        print "you passed the career"
        currentLevel = gameInfo.getCurrentLevel()
        gameInfo.getPlayer(0).setHighestLevel(currentLevel + 1)
    print "exiting"
    return gameInfo

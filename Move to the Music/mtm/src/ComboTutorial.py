"""
   ComboTutorial is based on CareerMode -- it plays one specific song
   and gives the basics of one specific combo.
"""

"""
   Begun 23 April 2008 by Jason Cisarano -- based on CareerMode.py
   27 April 2008 -- fixed end of tutorial so that it doesn't wait for end of song.
"""

from Controller import Controller
from GoodStep import GoodStep
from FileLocations import FileLocations
from ScreenBorder import ScreenBorder
from GameInfo import GameInfo
from SoundEffectController import SoundEffectController
from SongChooserMenu import ScreenInfo
from ComboDictionary import ComboDictionary
from GoodStep import GoodStep
from Combo import Combo
from Score import Score
from bisect import bisect
import CareerStatScreen
import random
import sys
import os
import thread
import pygame

#takes a screen
def startGame(screen):
    gameInfo = GameInfo()
    screenInf = ScreenInfo()
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

    print HIT_TOL

    comboDictionary = ComboDictionary()
    fileLocs=FileLocations()
    scorer=Score()
    screenBorder=ScreenBorder(screen)

    #find one simple song for this
    songfile = fileLocs.songs+ "\TeQuieroMas.mp3"
    timefile = fileLocs.beats+ "\TeQuieroMas.times"
    
    #initialize pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024*2)
    pygame.init()
    music = pygame.mixer.music
    music.load(songfile)

    
    #initialize sound controller
    soundController = SoundEffectController()
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
    def UpdateScore(gameinfo, dt):
        
        
        #set points per hit
        gameStats.setPointsPerHit(int(scorer.scoreHit(gameStats.getGoodSteps(),difficulty, dt, gameStats.getCurrentCombo())))
    
        currentScore = gameStats.getCurrentScore()
        
        pointsForCurrentHit = gameStats.getPointsPerHit()
        currentScore += pointsForCurrentHit
        
        gameStats.setCurrentScore(currentScore)
    
        
    def checkPositiveSounds(gameInfo):
        playPointsSound(gameInfo)
        

    #plays number of points based on how many points there are, every 100,000
    def playPointsSound(gameInfo):
        pass
        """
        totalScore = gameInfo.getCurrentScore()
        pointGoal = gameInfo.getPointGoal()
        if totalScore >= pointGoal:
            soundController.playNumberSound(totalScore)
            print "you've reached " + str(pointGoal) + " points!"
            gameInfo.setPointGoal(pointGoal + 100000)
         """
    
    #depending on the level, create a list of combos to ask for        
#    def createAskComboList(gameInfo):
#        #easy
#        comboListtoAsk = []
#            
#        unlockLevel = gameInfo.getCurrentLevel()
#        #unlockLevel = 9
#        print "highest level is " + str(unlockLevel)
#        
#        if unlockLevel ==0 or unlockLevel ==1: 
#            combos= comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
#            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
#            comboListtoAsk = combos + combos1
#        
#        elif unlockLevel ==2 or unlockLevel ==3:
#            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
#            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
#            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
#            comboListtoAsk = combos + combos1 + combos2
#            
#        elif unlockLevel ==4 or unlockLevel ==5:
#            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
#            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
#            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
#            combos3 = comboDictionary.getCombosOfSizeAndDifficulty(4, "easy")
#            comboListtoAsk = combos + combos1 + combos2 + combos3
#
#            
#        elif unlockLevel ==6 or unlockLevel ==7:
#            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
#            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
#            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
#            combos3 = comboDictionary.getCombosOfSizeAndDifficulty(4, "easy")
#            combos4 = comboDictionary.getCombosOfSizeAndDifficulty(4, "medium")
#            combos5 = comboDictionary.getCombosOfSizeAndDifficulty(4, "hard")
#            combos6 = comboDictionary.getCombosOfSizeAndDifficulty(5, "easy")
#            comboListtoAsk = combos + combos1 + combos2 + combos3 + combos4 + combos5 + combos6 
#            
#        elif unlockLevel ==8 or unlockLevel ==9:
#            combos = comboDictionary.getCombosOfSizeAndDifficulty(3, "easy")
#            combos1 = comboDictionary.getCombosOfSizeAndDifficulty(3, "medium")
#            combos2 = comboDictionary.getCombosOfSizeAndDifficulty(3, "hard")
#            combos3 = comboDictionary.getCombosOfSizeAndDifficulty(4, "easy")
#            combos4 = comboDictionary.getCombosOfSizeAndDifficulty(4, "medium")
#            combos5 = comboDictionary.getCombosOfSizeAndDifficulty(4, "hard")
#            combos6 = comboDictionary.getCombosOfSizeAndDifficulty(5, "easy")
#            combos7 = comboDictionary.getCombosOfSizeAndDifficulty(5, "medium")
#            combos8 = comboDictionary.getCombosOfSizeAndDifficulty(5, "hard")
#            comboListtoAsk = combos + combos1 + combos2 + combos3 + combos4 + combos5 + combos6 + combos7 + combos8
#        
#        
#        
#        gameInfo.setAskedComboList(comboListtoAsk)
#        

    def askForCombo(gameInfo):
        #get a combo to be played, randomly from askedComboList

        comboList = gameInfo.getAskedComboList()
        gameInfo.setAskedCombo(comboList[random.randrange(0,(len(comboList)))])
        combo = gameInfo.getAskedCombo()
        
        soundController.queueSoundFile(fileLocs.careerSounds+ "\\tryCombo.ogg")
        playComboSteps(combo)
        
        
        print "Let's try doing a combo! " + combo.getName()
        print combo.getStepNameList()

    def askForWarmupCombo():
        soundController.queueSoundFile(fileLocs.careerSounds + "\\tryCombo.ogg")
        playComboSteps(warmupCombo)
        
    def playComboSteps(combo):   
        steps = combo.getSteps()
        for step in steps:
            soundController.queueSoundFile(step.getSoundFile())
                 
    def checkForAskedCombo(gameInfo):
        if gameInfo.getCurrentCombo() == warmupCombo:
            print "Great Job, you hit the combo!"
            gameInfo.setAskedCombosHit(gameInfo.getAskedCombosHit() + 1)
            gameInfo.setAskedCombo(None)
            global hitWarmup
            return True
        return False
            
    def comboProcessing():
        gameStats.setCurrentCombo(CheckForCombo())
        if (gameStats.getCurrentCombo() != None):
            soundController.playComboInSong(gameStats.getCurrentCombo())
            gameStats.clearComboSteps()
            return True
        return False
            
    def stepProcessing(currentStep):
        gameStats.addStep(currentStep)
        gameStats.setBeatsHit(gameStats.getBeatsHit() + 1)
        gameStats.setBeatsAttempted(gameStats.getBeatsAttempted() + 1)
        soundController.playHitSound()      
            
    def missedBeat():
        gameStats.setBeatsAttempted(gameStats.getBeatsAttempted() + 1)
        gameStats.clearGoodSteps()
        gameStats.clearComboSteps()
                           
    def playNextPrompt( state, time ):
        """
           Takes needed action for given state, returns next appropriate state
        """

        if state == 0:
            if music.get_pos() - time > 5000: # makes sure there's always a bit of a pause -- tweak for each one
                soundController.queueSoundFile(fileLocs.menuSounds + "\menu_07_01.ogg")
                return (1, music.get_pos() ) #updated state and time
            return( 0, time )#no change to state or time
            
        if state == 1:
            if music.get_pos() - time > 9000:
                soundController.queueSoundFile(fileLocs.menuSounds + "\menu_07_03.ogg")
                return (2, music.get_pos() )
            return( 1, time )
            
        if state == 2:
            if music.get_pos() - time > 5000:
                soundController.queueSoundFile(fileLocs.menuSounds + "\menu_07_02.ogg")
                return (3, music.get_pos() )
            return( 2, time )
            
        if state == 3:
            if music.get_pos() - time > 5000:
                askForWarmupCombo()
                return (4, music.get_pos() )
            return( 3, time )
            
        if state == 4:
            if music.get_pos() - time > 15000:
                soundController.queueSoundFile(fileLocs.menuSounds + "\menu_07_07.ogg")
                return (3, music.get_pos() )
            return (4, time)       
        
        if state == 5:
            if time != -1:       
                soundController.queueSoundFile(fileLocs.menuSounds + "\menu_07_05.ogg")
                soundController.queueSoundFile(fileLocs.menuSounds + "\menu_07_06.ogg")
            return (5, -1)
        
    #start the single player mode and initialize
    music.set_volume(.5)
    music.play()
    errors = []
    cntrl=Controller()
    #createAskComboList(gameInfo)
    
      #tutorial-specific vars
    promptState = 0
    lastPromptTime = 0
    hitWarmup = False    
    warmupCombo = Combo((GoodStep(6), GoodStep(7), GoodStep(6)) , "Warm_Er_Up" )
        
#    timeSinceCombo = 0
#    timeOfCombo = 0
#    repeatedCombo = False
    
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
        
        if music.get_pos() > 4000:
            if not soundController.isPlaying():
                promptState, lastPromptTime = playNextPrompt( promptState, lastPromptTime )
#                timeOfCombo= t
 
        soundController.update()
        if hitWarmup:
#            run = False
            if not soundController.isPlaying() and promptState == 5:
                run = False
            else:
                promptState = 5
       
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
                    hitWarmup = comboProcessing()
                             
                    #update the score
                    UpdateScore(gameInfo, dt)
                    checkPositiveSounds(gameInfo)

                else:
                    #clear the goodSteps and combo list, because you stepped on a wrong beat
                    missedBeat()
                
        else:
            pygame.time.wait(2)
        
        clock.tick(30)
        FlashOrUpdateScreen(gameStats)
       # soundController.update()
        gameStats.setCurrentCombo(None)
            
    music.fadeout(4000)
        
    print "exiting"
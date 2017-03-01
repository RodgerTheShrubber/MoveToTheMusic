"""
   Score hold a class with variables representing a base score as well as tolerances for 
   the various degrees of good hits
"""

"""
   Score started 12 Feb by Trey Brumley -- created a basic score system that would increment the score
   by a constant amount
   
   edited 20 Feb by Trey Brumley= included multipliers based on the following
   -how close you were to the beat
   -how much further away your current step is from your last one
   -how many different steps you had in the last 5 moves
   -COMBOS
"""

import pygame
import os
import sys
import string
from FileLocations import FileLocations


BASE_SCORE=100
PERFECT_SCORE = .15
GOOD_SCORE = .25
FAIR_SCORE = .3

class Score():
    """
       Score hold a class with variables representing a base score as well as tolerances for 
       the various degrees of good hits
    """
    
    
 
    def scoreHit(self,goodStep,difficulty,time,combo):
        
        if (difficulty ==0):
            PERFECT_DIFF = .15
            GOOD_DIFF = .25
            FAIR_DIFF = .3
        
        if (difficulty ==1):
            PERFECT_DIFF = .1
            GOOD_DIFF = .2
            FAIR_DIFF = .25
        
        if (difficulty ==2):
            PERFECT_DIFF = .05
            GOOD_DIFF = .15
            FAIR_DIFF = .2
      
        currentScore=BASE_SCORE
            #based on how close the step was to the beat-increase/decrease their score
        if(time<PERFECT_DIFF):
           currentScore=BASE_SCORE*2
        elif(time<GOOD_DIFF):
            currentScore=BASE_SCORE*.75
        else:
            currentScore=BASE_SCORE*.5
            #compare the current step to the last step and get the difference from the tuple
        atStep=goodStep[len(goodStep)-1]
        lastStep=goodStep[len(goodStep)-2]
        if(atStep==None):
            return 0
        if(lastStep==None):
            return BASE_SCORE
        if(len(goodStep)>1):
            x1,y1=atStep.location
            x2,y2=lastStep.location
            currentScore*=(1+abs(x1-x2)+abs(y1-y2))
        #multiply the current score by the amount of unique steps
        uniqueX=1
        for steps in goodStep:
            isUnique=True
            oneChance=True
            for compareStep in goodStep:
                if(compareStep==None):
                    isUnique=False
                if(compareStep!=None and steps!=None and compareStep.location==steps.location ):
                    if(oneChance):
                        oneChance=False
                    else:
                        isUnique=False
            if(isUnique):
                uniqueX+=1
        currentScore *= uniqueX
        
        #multiply by combo multiplier
        currentScore *= self.getComboMultiplier(combo)
        
        return currentScore
    
    #takes a combo and returns a multiplier for it
    def getComboMultiplier(self,combo):
        if (combo == None):
            return 1
        currentCombo = combo
        multiplier = 5 * currentCombo.getNumberOfSteps()
        return multiplier
        
        
        
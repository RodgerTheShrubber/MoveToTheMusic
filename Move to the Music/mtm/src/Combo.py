"""
    This class represents a combo in the game.  It is a list of goodsteps that
    a player must hit in order, and a name of the combo.  There is also a sound
    file that follows the convention of being a .ogg file and being named after the combo.
    
"""

import sys
import os
import pygame
from Score import Score
from FileLocations import FileLocations
from pygame.locals import *

class Combo:
    
    #should input the number of steps in the combo, and a list of goodsteps that make up the combo, separated by
    #commas.  It should also have a sound file associated with it
    def __init__(self, goodSteps, comboName):
        
        self.comboSteps = []
        self.comboSteps = goodSteps
        self.numberOfSteps = len(self.comboSteps)
        self.name = comboName
        self.fileLocs = FileLocations()
        self.scorer = Score()
        self.difficulty = 0
        self.difficultyBenchmarks = {"easy": 40000 , "medium":70000 , "hard": 2000000}
        
        
    
    def getNumberOfSteps(self):
        """
        returns int number of steps
        """
        self.numberOfSteps
        return self.numberOfSteps

    
    def getSteps(self):
        """
        returns the list representation of the goodsteps in the combo
        """
        return self.comboSteps
    
    
    def getName(self):
        """
        returns the name of the combo
        """
        return self.name
    
    def getStepNameList(self):
        """
        return the list representation of buttons (topRight, left, etc)
        """
        nameList = []
        for step in self.getSteps():
            nameList.append(step.getName()) 
            
        return nameList
        
    
    def getComboSoundFile(self):
        """
        return path of the sound file, the sound file should follow the convention of
        having the same name as the combo
        """
        path = self.fileLocs.comboSounds
        path = path + "\\" + self.getName() + ".ogg"
        return path
    
    def getDifficulty(self):
        """
        returns a difficulty for the combo, easy, medium, or hard, based on difficulty benchmarks in combo
        """
        stepsList = self.getSteps()
        difficultyNumber = self.scorer.scoreHit(stepsList,2, .01, self)
        difficulty = ""
        if difficultyNumber<= self.difficultyBenchmarks["easy"]:
            difficulty = "easy"
        elif difficultyNumber <= self.difficultyBenchmarks["medium"]:
            difficulty = "medium"
        elif difficultyNumber <= self.difficultyBenchmarks["hard"]:
            difficulty = "hard"
        
        return difficulty
    
    def __str__(self):
        return str(self.comboSteps)
        
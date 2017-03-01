"""
Creates a dictionary of all the combos in the game.  Can retrieve combos of a certain size,
of a particular difficulty, or both.
"""


from FileLocations import FileLocations
from GoodStep import GoodStep
from Combo import Combo
import sys
import os
from sets import Set

class ComboDictionary():
    def __init__(self):
        fileLocs = FileLocations()
        prefix = fileLocs.comboSounds
        zero = GoodStep(0)
        one = GoodStep(1)
        two = GoodStep(2)
        three = GoodStep(3)
        five = GoodStep(5)
        six = GoodStep(6)
        seven= GoodStep(7)
        eight = GoodStep(8)
        
        
        comboA = Combo((six,seven,six), "Warm_Er_Up")
        comboB = Combo((six,three,zero),"Jackhammer")
        comboC = Combo((seven,six,three),"Sidewinder")
        comboD = Combo((seven,five,eight ),"Off_The_Rocker")
        comboE = Combo((one,six,eight),"Chromosomal")
        comboF = Combo((one,eight,six),"Corkscrew")
        comboG = Combo((three,five,seven),"Whirlwind")
        comboH = Combo((three,zero,three), "Left_Waggle")
        comboI = Combo((five,eight,five), "Right_Waggle")
        comboJ = Combo((five,zero,three), "Sicktackular")
        comboK = Combo((two,seven,six), "Thunderstorm")
        comboL = Combo((two,five,eight), "Triple_Jump")
        comboM = Combo((zero,one,two), "Super_Slide")
        comboN = Combo((zero,two,five), "ZigZag")
        comboO = Combo((eight,seven,six), "Exit_Hatch")
        comboP = Combo((eight,three,one), "Blast_Off")
        comboQ = Combo((six,three,seven,seven),"Power_Surge")
        comboR = Combo((seven,one,three,five),"Inferno")
        comboS = Combo((eight,five,five,eight),"Carolina_Two_Step")
        comboT = Combo((three,six,seven,two),"Torpedo")
        comboU = Combo((five,two,one,five),"Fusion")
        comboV = Combo((zero,zero,three,one),"Somersault")
        comboW = Combo((one,six,seven,eight),"Psycho_T")
        comboX = Combo((two,eight,two,zero),"Ricochet")
        comboY = Combo((six,eight,two,zero,six),"Atomic_Accelerator")
        comboZ = Combo((seven,five,one,three,seven),"Flipside_360")
        comboAA = Combo((eight,five,seven,three,six),"Berserker")
        comboBB = Combo((three,zero,three,one,three),"Canonball")
        comboCC = Combo((five,eight,six,three,two),"Schism_Leap")
        comboDD = Combo((zero,one,zero,one,zero),"Running_Man")
        comboEE = Combo((one,two,zero,one,one),"Suspended_In_Time")
        comboFF = Combo((two,eight,five,three,seven),"Annihilator")
        
        
        self.comboDictionary= [comboA,comboB,comboC,comboD,comboE,comboF,comboG,comboH,\
                               comboI, comboJ, comboK, comboL, comboM, comboN, comboO, comboP,\
                               comboQ,comboR,comboS,comboT,comboU,comboV,comboW,comboX,comboY, \
                               comboZ,comboAA,comboBB,comboCC,comboDD,comboEE,comboFF]
        self.MINCOMBO = 3
        self.MAXCOMBO = 5
   
        self.combosSize3 = self.createCombosOfSize(3)    
        self.combosSize4 = self.createCombosOfSize(4) 
        self.combosSize5 = self.createCombosOfSize(5)   
        
       
       
    def getDictionary(self):
        """
        get all the combos in the dictionary and return them in a list form
        """
        return self.comboDictionary
    
    def createCombosOfSize(self, size):
        """
        private function used to create lists of combos of a particular song
        """
        a = size
        comboDictionaryTemp = []
        if a < self.MINCOMBO:
            a = self.MINCOMBO
        if a > self.MAXCOMBO:
            a = self.MAXCOMBO
            
        for combo in self.comboDictionary:
            if combo.getNumberOfSteps() == a:
                comboDictionaryTemp.append(combo)
                
        return comboDictionaryTemp
    
    def getCombosOfSize(self,size):
        """
        returns combos of a certain size as a list, or returns None if there are none of that size.  Should be 3,4, or 5
        """
        if size == 3:
            return self.combosSize3
        elif size == 4: 
            return self.combosSize4
        elif size == 5:
            return self.combosSize5
        else:
            return None
    
    def getCombosOfDifficulty(self, difficulty):
        """
        returns combos of a certain difficulty as a list, must be easy, medium, or hard
        """
        diff = difficulty
        tempComboList = []
        if diff != "easy" and diff != "medium" and diff!= "hard":
            print "you need to make it easy, medium, or hard"
            return None
        for combo in self.comboDictionary:
            if combo.getDifficulty() == diff:
                tempComboList.append(combo)
        
        return tempComboList
    
    def getCombosOfSizeAndDifficulty(self, size, difficulty):
        """
        retuns combos of a size and difficulty
        """
        sizeList = self.getCombosOfSize(size)
        diffList = self.getCombosOfDifficulty(difficulty)
        
        return list(set(sizeList) & set(diffList))
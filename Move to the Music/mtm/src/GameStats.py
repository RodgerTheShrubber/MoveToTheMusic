class GameStats(object):

    def __init__(self):
        #all stuff for a particular level
        
        self.__MAXSTEPS = 5
        self.__currentScore = 0  
        self.__pointsPerHit = 75
        self.__currentCombo = None
        self.__goodSteps = []
        self.__comboSteps = []     
        self.__beatsHit = 0
        self.__beatsAttempted = 0
        self.__combosHit = 0
        self.__askedCombosHit = 0
        self.__askComboList = []
        self.__askedCombo = None  
        self.__pointGoal = 100000
        
        
    def getPointGoal(self):
        return self.__pointGoal
    
    def setPointGoal(self, pointGoal):
        self.__pointGoal = pointGoal
        
    def getAskedComboList(self):
        return self.__askComboList
    
    def setAskedComboList(self, list):
        self.__askComboList =list

    def getBeatsHit(self):   
        return self.__beatsHit
        
    def getBeatsAttempted(self):   
        return self.__beatsAttempted
    
    def getCombosHit(self):   
        return self.__combosHit   
    
    def getAskedCombo(self):
        return self.__askedCombo
    
    def getCurrentCombo(self):
        return self.__currentCombo

    
    def getCurrentScore(self):
        return self.__currentScore
    
    def getPointsPerHit(self):
        return self.__pointsPerHit
    
    def getGoodSteps(self):
        return self.__goodSteps
    
    def getComboSteps(self):
        return self.__comboSteps
    
    def getMaxSteps(self):
        return self.__MAXSTEPS

    def getAskedCombosHit(self):
        return self.__askedCombosHit
    
    def setAskedCombosHit(self, number):
        self.__askedCombosHit= number
    
    def setAskedCombo(self, combo):
        self.__askedCombo = combo
    
    
    def setCurrentCombo(self, combo):
        self.__currentCombo = combo
        
        
    def setCurrentScore(self, score):
        """
           If input 0 < score, save that score.  Returns false if score not
           set.
        """
        if(0 <= score):
            self.__currentScore = score
            return True
        else:
            return False

    
    def setPointsPerHit(self, pointsperhit):
        self.__pointsPerHit = pointsperhit
    
    def setGoodSteps(self, stepList):
        self.__goodSteps = stepList
    
    def setComboSteps(self, stepList):
        self.__comboSteps = stepList
        
    def setBeatsHit(self, number):   
        self.__beatsHit = number
        
    def setBeatsAttempted(self, number):   
        self.__beatsAttempted = number
    
    def setCombosHit(self, number):   
        self.__combosHit = number 
          
    
    #see if goodSteps is greater than the maximum # you want to keep track of, if it is, pop the stack        
    def addStep(self, step):
        """
           see if goodSteps is greater than the maximum # you want to keep track of, if it is, pop the stack
        """
        self.__goodSteps.append(step)
        self.__comboSteps.append(step)
        
        if len(self.__goodSteps) > self.__MAXSTEPS: 
            self.__goodSteps.pop(0)
        if len(self.__comboSteps) > self.__MAXSTEPS:
            self.__comboSteps.pop(0)
            
    def clearGoodSteps(self):
        del self.__goodSteps[:]
        
    def clearComboSteps(self):
        del self.__comboSteps[:]
        
        
    def newRound(self):
        """
           Reset all data items tracked during song.
        """
        self.clearGoodSteps()
        self.clearComboSteps()
        self.setCurrentCombo(None)
        self.setAskedCombo(None)
        self.setAskedComboList(None)
        self.setAskedCombosHit(0)
        self.setCurrentScore(0)
        self.setBeatsHit(0)
        self.setBeatsAttempted(0)
        self.setCombosHit(0)
        self.setPointsPerHit(75);
        
        

"""
   GoodStep holds all the information we need a step to have _after_ it has been verified 
   as "interesting" byController.checkStep().
"""

"""
   GoodStep started 15 Feb by Jason Cisarano -- created constructor, attributes, several getters and setters
   16 Feb added stepLocations as tuples
"""
"""
   Step locations laid out as follows in (x,y) pairs starting in the bottom left corner:
   =========================
   |  0,2  |  1,2  |  2,2  |
   =========================
   |  0,1  |  XX   |  2,1  |
   =========================
   |  0,0  |  1,0  |  2,0  |
   =========================
"""
from FileLocations import FileLocations

class GoodStep(object):
    "Container for information about a valid step."

    def __init__ (self, location, time=0):
        """
            Location must be a int, which is converted to a tuple, time is the time since the current song began.  If no song is playing
             (i.e. during menu navigation), default time = 0.
        """
        self.stepLocations = {0:(0, 0), 1:(1, 0), 2:(2, 0), 3:(0, 1), 5:(2, 1), 6:(0, 2), 7:(1, 2), 8:(2, 2)}
        self.stepDictionary = {(0, 0): "back-left",(1, 0):"back",(2, 0):"back-right",(0, 1): "left",\
                            (2, 1):"right",(0, 2):"front-left",(1, 2):"front", (2, 2):"front-right"}
        self.__buildLocation(location)
        self.fileLocs = FileLocations()
        self.time = time

    def getTime(self):
        "Returns the time the original step event was created."
        return self.time
    
    def getLocation(self):
        "The location on the x-y mat grid of where the step hit as a tuple."
        return self.location
    
    def getName(self):
        """
           Returns name of this step as string
        """
        return self.stepDictionary[self.getLocation()]
    
    def getSoundFile(self):
        path = self.fileLocs.stepSounds
        path = path + "\\" + self.getName() + ".ogg"
        return path
    
    def __buildLocation(self, location):
        "Finds place on grid and sets location as tuple with x,y coords starting in bottom-left of grid"
        self.location=self.stepLocations[location]
    def __str__(self):
        "returns the location of the step"
        return str(self.location)
        
    
    
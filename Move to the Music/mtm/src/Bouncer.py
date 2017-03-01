"""
   Calculates and storyes x,y coordinates for an item that bounces up and down based on sinusiodal curve.
   It does not hold the graphical item to be animated.
"""

"""
   Begun 5 April by Jason Cisarano.  Included complete setBounce, getCoord, and isBouncing functions.
"""

from math import sin, pi
import pygame

class Bouncer(object):
    """
       Calculates and storyes x,y coordinates for an item that bounces up and down based on sine curve.
       Amount and time of bounce is predetermined. It does not hold the graphical item to be animated.
    """    
    
    def __init__(self, x,y):
        """
           Set initial state -- expects starting x, y values
        """
          #tweakable settings
        self.__period = 300 ####time in milliseconds for cycle
        self.__displacement = 50 ###how far to move up and down
        
          #state variables
        self.__isBouncing = False
        self.__y_original = y
        self.__y = y
        self.__x = x
        self.__startTime = 0
        
        self.__frequency = pi /(self.__period) 
    
    def setBounce(self):
        """
           Used to set this Bouncer to bounce status so that it will
           automatically begin moving with subsequent calls to getCoords.
        """
        if not self.__isBouncing:
            self.__startTime = pygame.time.get_ticks()
            self.__isBouncing = True
            
    def isBouncing(self):
        """
           Returns the bouncing state of this Bouncer.
        """
        return self.__isBouncing
    
    def getCoords(self):
        """
           Returns x,y coordinates of this Bouncer as a tuple (x,y).
           If this Bouncer is currently bouncing, the y value will reflect
           this automatically.
        """
        if self.__isBouncing:
            self.__updateY()
        return (self.__x, self.__y)
    
    def __updateY(self):
        """
           Sets y value of bouncing item as function of time since bounce began.
           On end of bounce, updateY returns y value to original baseline and 
           sets bounce status to False.
        """
        if self.__isBouncing:
            elapsedTime = pygame.time.get_ticks() - self.__startTime
#            print "Frequency = " + self.__frequency.__str__()
#            print "Current time = " + pygame.time.get_ticks().__str__()
#            print "Start time = " + self.__startTime.__str__()
#            print "Elapsed time = " + elapsedTime.__str__()
#            print "elapsedTime * frequency =" + (elapsedTime * self.__frequency).__str__()
            if elapsedTime < self.__period:
                f = sin(-(abs(elapsedTime * self.__frequency))) 
#                print "f = " + f.__str__()
                self.__y = int(f * self.__displacement + self.__y_original)
            else:
                self.__y = self.__y_original
                self.__isBouncing = False


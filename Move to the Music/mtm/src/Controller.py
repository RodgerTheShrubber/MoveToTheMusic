"""
 Controller handles input from the keyboard and from the dance mat.  It checks an incoming event
 and looks for events relevant to the game.  When it finds a relevant event, it returns a GoodStep
 object initialized with the proper information.  To use this, create a Controller object in your code
 and then just call checkEvent( event, time ).  This class will will automatically initialize joysticks if needed.
"""

"""
 Created 15 Feb by Jason Cisarano.  Created basic attributes and methods.  16 Feb added support for mat.
"""

"""
'Interesting' keycodes:
numpad:
7-263  8-264  9-265
4-260  5-261  6-262
1-257  2-258  3-259

letters:
q-113  w-119  e-101
a-97   s-115  d-100
z-122  x-120  c-99

arrows:
left-113
right-113
down-113
up-113
"""

"""Dance mat button numbers:
===================
|  8  |  xx  |  9  |
===================
|  2  |  12  |  1  |
===================
|  15 |  XX  |  13 |
===================
|  0  |  14  |  3  |
===================
"""

import pygame
from pygame.locals import *
from GoodStep import GoodStep

class Controller (object):
    """
       Controller handles input from the keyboard and from the dance mat.  It checks an incoming event
       and looks for events relevant to the game.  When it finds a relevant event, it returns a GoodStep
       object initialized with the proper information.  To use this, create a Controller object in your code
       and then just call checkEvent( event, time ).  This class will will automatically initialize joysticks if needed.
      
       Initializes joystick if needed, handles controller input.
    """

    def __init__(self, player=1):
        """
           Sets up needed elements for controller.
        """
        if player == 1:
            result=None
            #keycodes correspond to letters in this order: z, x, c, a, d, q, w, e
            self.keyCodes=[122, 120, 99, 97, 100, 113, 119, 101 ]
            #stepValues map keycodes to our standard output 0-8
            self.keyStepValues={122:0, 120:1, 99:2, 97:3, 100:5, 113:6, 119:7, 101:8, 276:3,275:5,273:7,274:1}
            #these are the button values returned by JOYBUTTONDOWN.button
            self.matCodes=[0, 14, 3, 15, 13, 2, 12, 1]
            #maps button values to our standard values that match key values above
            self.matStepValues={0:0, 14:1, 3:2, 15:3, 13:5, 2:6, 12:7, 1:8}
            #maps button values to our standard values that match key values above
            #self.wiiButtonValues={"LEFT":3, "UP:7", "DOWN:1","RIGHT:5",}
            self.__initializeJoystick()
        #if you say this is player 2, then these are the buttons
        elif player == 2:
            result=None
            #keycodes correspond to letters in this order: z, x, c, a, d, q, w, e
            self.keyCodes=[122, 120, 99, 97, 100, 113, 119, 101 ]
            #stepValues map keycodes to our standard output 0-8
            self.keyStepValues={122:0, 120:1, 99:2, 97:3, 100:5, 113:6, 119:7, 101:8, 276:3,275:5,273:7,274:1}
            #these are the button values returned by JOYBUTTONDOWN.button
            self.matCodes=[0, 14, 3, 15, 13, 2, 12, 1]
            #maps button values to our standard values that match key values above
            self.matStepValues={0:0, 14:1, 3:2, 15:3, 13:5, 2:6, 12:7, 1:8}
            #maps button values to our standard values that match key values above
            #self.wiiButtonValues={"LEFT":3, "UP:7", "DOWN:1","RIGHT:5",}
            self.__initializeJoystick()
            """
            result=None
            #keycodes correspond to letters in this order: m,.jkluio
            self.keyCodes=[109,44, 46, 170, 172, 117, 105, 106]
            #stepValues map keycodes to our standard output 0-8
            self.keyStepValues={109:0, 44:1, 46:2, 170:3, 172:5, 117:6, 105:7, 106:8}
            #these are the button values returned by JOYBUTTONDOWN.button
            self.matCodes=[0, 14, 3, 15, 13, 2, 12, 1]
            #maps button values to our standard values that match key values above
            self.matStepValues={0:0, 14:1, 3:2, 15:3, 13:5, 2:6, 12:7, 1:8}
            self.__initializeJoystick()
            """
            
            
        
    def __initializeJoystick(self):
        "Scans joysticks present and initializes them using pygame routine"
        joysticks = []
        for joystick_no in xrange(pygame.joystick.get_count()):
            stick = pygame.joystick.Joystick(joystick_no)
            stick.init()
            joysticks.append(stick)
            
    def checkEvent(self, event, time=0):
        """
          Looks at keyboard, mouse and joystick events and determines if they're useful.
          When it finds a good event, it returns a GoodStep object with appropriate info.
          Event is the event to check, time is the time between the beginning of the current
          song and the event.  If there is no song (e.g. during menu navigation, the default 
          value is used.
        """
        self.time = time
        if event.type is (JOYBUTTONDOWN):
            self.__convertJoyButtonDown(event)     
        elif event.type is (KEYDOWN):
            self.__convertKeyDown(event)
        #elif event.type == pygame_wiimote.WIIMOTE_BUTTON_PRESS:
        #    self.__convertWiiButton (event)
        #elif event.type == pygame_wiimote.WIIMOTE_ACCEL:
        #    self.__convertWiiMoteEvent (event)
        elif event.type == QUIT:
            #add exit confirmation dialog and maybe savegame options
            exit()
        else:    
            return None #the Python version of null
        
          #got this far, so something good was found.  Return it
        return self.result
        
    def __convertKeyDown(self, event):
        """Shouldn't be called outside this class
            It checks key events against expected good events
            as listed in keyCodes.  When one is found,  
            it sets self.result to a new GoodStep item
            with the correct stepValue as defined in keyStepValues"""
          #first look for numbers on keypad
        if (256 < event.key) and (event.key < 261) or (261 < event.key) and (event.key < 266):
            self.result = GoodStep(event.key - 257, self.time)
        elif (96 < event.key) and (event.key < 123):  #then look for letter keys -- first rule out some hits
            #then iterate through good keys
            for item in self.keyCodes:
                if(event.key == item):
                    self.result = GoodStep(self.keyStepValues[item], self.time)
                    break #found a good key: no need to keep looking
                else:
                    self.result = None
        elif (272 < event.key < 277):
            self.result = GoodStep(self.keyStepValues[int(event.key)], self.time)
        else:
            print event.key
            self.result = None

    def __convertJoyButtonDown(self, event):
        """Shouldn't be called outside this class
           Checks button number against list of good buttons
           defined in matCodes and when one is found, assigns
           new GoodStep object to self.result with correct stepValue
           as defined in matStepValues"""
        for item in self.matCodes:
                if(event.button == item):
                    self.result = GoodStep(self.matStepValues[item], self.time)
                    break #found a good key: no need to keep looking
                else:
                    self.result = None
                    
    def __convertWiiMoteEvent(self, event):
        """Shouldn't be called outside this class
           Defines when the wii mote has hit its peak
           0 accelleration in one direction, but others are moving
           NOTE: this means if you push the wiimote in one direction it wont work
           (which most people will find unnatural)"""
        """
        hasBeat = False
        threshHold = 10
        totalAcc = 0
        for c in range(3):
            totalAcc += event.accel[c]
            if event.accel[c] == 0:
               hasbeat = True
        if threshHold * -1 <totalAcc or totalAcc>threshHold:
            self.result = GoodStep(self.matStepValues[0], self.time)
        else:
            self.result = None  
            """
    def __convertWiiButton(self, event):
        """Shouldn't be called outside this class
           Checks button number against list of good buttons
           defined in matCodes and when one is found, assigns
           new GoodStep object to self.result with correct stepValue
           as defined in matStepValues"""
        """
        if self.wiiButtonValues.count (event.button) != 0:
            self.result = GoodStep(self.wiiButtonValues[event.button], self.time)
        else:
            self.result = None  
        """
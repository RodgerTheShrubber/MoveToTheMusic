"""This class queues or plays any given sound file, and takes care of playing sounds during
the game.  
The difference between queue and play is as follows:
queue gets a sound ready to play and will play it if nothing else important is being played on the channel
play just plays a sound on a random channel

use queue for sounds that should be linked, and play for sounds that are just plain sound effects, like
bleeps or claps
"""


import pygame
import thread
from pygame.locals import *
from NumberSpeaker import NumberSpeaker
from FileLocations import FileLocations

class SoundEffectController(object):
    """
       This class queues or plays any given sound file, and takes care of playing sounds during
       the game.  
       The difference between queue and play is as follows:
       queue gets a sound ready to play and will play it if nothing else important is being played on the channel
       play just plays a sound on a random channel

       Use queue for sounds that should be linked, and play for sounds that are just plain sound effects, like
       bleeps or claps
    """
    def __init__(self, volume=1):
        pygame.mixer.init()
        
        self.fileLocs = FileLocations()
        self.numberSpeaker = NumberSpeaker()
        self.channel = pygame.mixer.Channel(1)
        self.soundQueue = []
        self.channel.set_volume(volume)
        
    def getChannel(self):
        return self.channel
    
    def setChannel(self,number):
        self.channel = pygame.mixer.Channel(number)
        
    def playHitSound(self):
        hitSound = pygame.mixer.Sound(self.fileLocs.soundEffects + "\\clap.wav")
        hitSound.play()
        
    def playMissSound(self):
        missSound = pygame.mixer.Sound(self.fileLocs.soundEffects + "\\SHRTALRM.wav")
        self.playSound(missSound)
    
    def playCombo(self, combo):
        comboSound = pygame.mixer.Sound(combo.getComboSoundFile())
        self.queueSound(comboSound)
        
    def playComboInSong(self, combo):
        
        comboWordSound = pygame.mixer.Sound(self.fileLocs.comboSounds + "\\combo.ogg")
        self.queueSound(comboWordSound)
        self.playCombo(combo)
    
    def playNumberSound(self,number):
       
        numberSoundList =self.numberSpeaker.getNumberSounds(number)
        for sound in numberSoundList:
            self.queueSound(sound)

        
    #takes a file, makes it a sound object and plays it
    def playSoundFile(self, soundFile):
        sound = pygame.mixer.Sound(soundFile)
        sound.play()
        
    #queues up a sound to play      
    def queueSoundFile(self, soundFile):
        self.soundQueue.append(pygame.mixer.Sound(soundFile))
        
    def playAllSounds(self):
        while len(self.soundQueue)!= 0:
            self.update()
        
    
    def playSound(self,sound):
        """
           plays a sound object
        """
        sound.play()
    #queues a sound object
    def queueSound(self, sound):
        self.soundQueue.append(sound)
    #clears the queue    
    def flush(self):
        self.channel.stop()
        self.soundQueue = []

    def update(self):
        if (self.getChannel().get_busy() == False):
            if len(self.soundQueue) > 0:
                currentSound = self.soundQueue[0]
                self.channel.play(currentSound)
                self.soundQueue.pop(0)
            else:
                return None
        print len(self.soundQueue)
            
    def isPlaying(self):
        """
           Returns true if this SoundEffectController is currently playing
           a sound file.  Otherwise returns false.
        """
        return self.getChannel().get_busy()
#        return self.soundQueue.__len__() > 0
            
        
    
    
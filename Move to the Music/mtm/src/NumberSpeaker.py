import sys
import os
import pygame

from FileLocations import FileLocations



class NumberSpeaker(): 
    def __init__(self):
        self.ones = ["", "one ","two ","three ","four ", "five ",
            "six ","seven ","eight ","nine "]
        self.tens = ["ten ","eleven ","twelve ","thirteen ", "fourteen ",
            "fifteen ","sixteen ","seventeen ","eighteen ","nineteen "]
        
        self.twenties = ["","","twenty ","thirty ","forty ",
            "fifty ","sixty ","seventy ","eighty ","ninety "]
        
        self.thousands = ["","thousand ","million ", "billion ", "trillion ",
            "quadrillion ", "quintillion ", "sextillion ", "septillion ","octillion ",
            "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ",
            "quattuordecillion ", "sexdecillion ", "septendecillion ", "octodecillion ",
            "novemdecillion ", "vigintillion "]   
        
        self.numberDictionary = {"one": "\\one.ogg", "two": "\\two.ogg", "three": "\\three.ogg", "four": "\\four.ogg", "five": "\\five.ogg",\
                                        "six": "\\six.ogg", "seven": "\\seven.ogg", "eight": "\\eight.ogg", "nine": "\\nine.ogg",\
                                        "ten": "\\ten.ogg", "eleven": "\\eleven.ogg", "twelve": "\\twelve.ogg", "thirteen": "\\thirteen.ogg",\
                                        "fourteen": "\\fourteen.ogg", "fifteen": "\\fifteen.ogg", "sixteen": "\\sixteen.ogg",\
                                        "seventeen": "\\seventeen.ogg", "eighteen": "\\eighteen.ogg", "nineteen": "\\nineteen.ogg",\
                                        "twenty": "\\twenty.ogg", "thirty": "\\thirty.ogg", "forty": "\\forty.ogg",\
                                        "fifty": "\\fifty.ogg", "sixty": "\\sixty.ogg", "seventy": "\\seventy.ogg",\
                                        "eighty": "\\eighty.ogg", "ninety": "\\ninety.ogg", "hundred": "\\hundred.ogg",\
                                        "thousand": "\\thousand.ogg", "million": "\\million.ogg", "billion": "\\billion.ogg"}
        
    def int2word(self,n):
        # integer number to english word conversion
        # can be used for numbers as large as 999 vigintillion
        # (vigintillion --> 10 to the power 60)
        # tested with Python24      vegaseat      07dec2006


        #code taken from http://www.daniweb.com/code/snippet609.html, by vegaseat
        """
        convert an integer number n into a string of english words
        """
        # break the number into groups of 3 digits using slicing
        # each group representing hundred, thousand, million, billion, ...
        n3 = []

        # create numeric string
        ns = str(n)
        for k in range(3, 33, 3):
            r = ns[-k:]
            q = len(ns) - k
            # break if end of ns has been reached
            if q < -2:
                break
            else:
                if  q >= 0:
                    n3.append(int(r[:3]))
                elif q >= -1:
                    n3.append(int(r[:2]))
                elif q >= -2:
                    n3.append(int(r[:1]))

        
        #print n3  # test
        
        # break each group of 3 digits into
        # ones, tens/twenties, hundreds
        # and form a string
        nw = ""
        for i, x in enumerate(n3):
            b1 = x % 10
            b2 = (x % 100)//10
            b3 = (x % 1000)//100
            #print b1, b2, b3  # test
            if x == 0:
                continue  # skip
            else:
                t = self.thousands[i]
            if b2 == 0:
                nw = self.ones[b1] + t + nw
            elif b2 == 1:
                nw = self.tens[b1] + t + nw
            elif b2 > 1:
                nw = self.twenties[b2] + self.ones[b1] + t + nw
            if b3 > 0:
                nw = self.ones[b3] + "hundred " + nw
        return nw
    
    def loadAudio(self):
            """
            Loads voice files for the numbers
            """
            
            self.numberChannel = pygame.mixer.Channel(0)
    
    #takes a written out representation of a number and loads the associated sound files
    def getNumberSounds(self, number):
        numberWord = self.int2word(number)
        fileLocs=FileLocations()
        numberWordArray = numberWord.split()
        SoundFileArray = []
        
        for word in numberWordArray:
            filename = self.numberDictionary[word]
            SoundFileArray.append(pygame.mixer.Sound(fileLocs.numberSounds+filename))
        
        return SoundFileArray
        
        #self.numberChannel.play(pygame.mixer.Sound(fileLocs.numberSounds+filename))
        
    #given an integer, plays the written out representation of the word 
    def speakNumber(self,number):
        self.loadAudio()
        numberSounds = self.getNumberSounds(number)
        
        #for each word, queue the word and play it
        for sound in numberSounds:
            #self.soundController.playSequenceSound
            
            while(self.numberChannel.get_busy() == True):
                pygame.time.wait(3)
                
            #self.numberChannel.play(sound)
            
                
        
        
       
        
        
        
        



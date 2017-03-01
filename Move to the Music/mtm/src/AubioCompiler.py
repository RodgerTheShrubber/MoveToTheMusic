#This class makes aubio compile a song -- it has to be a wav file, however
#something weird happens with mp3s, even if it thinks it will work
#one problem with this script is that it expects the song to be in the folder
#where aubiotrack is, but we can fix all that.
import os
#import tkFileDialog
import shutil
import sys
import re
from FileLocations import FileLocations
import pygame
from SoundEffectController import SoundEffectController


soundController = SoundEffectController()
fileLoc = FileLocations()
currentDir = os.curdir
mysongs = []
oldSongs =[]

def getOldSongs(sms,dr,flst):
    for file in flst:
        wholeFile = os.path.splitext(file.__str__())
        if (wholeFile[1] == ".mp3"):
            oldSongs.append(wholeFile[0])
            
def changeNames(sms,dr,flst):
    if (len(flst) == 0):
       # soundController.queueSound(pygame.mixer.Sound(fileLoc.nameEntry+r"\menu_14_01.ogg"))
        #soundController.playAllSounds()
        testasdfsa=1
    for file in flst:
        songName = os.path.splitext(file.__str__())[0]
        ext = os.path.splitext(file.__str__())[1]
        print songName
        newName = songName.replace(" ", "_")
        newName = newName.replace ("-","_")
        if (newName != songName):
            try:
                print 'adding .',fileLoc.songslist+"\\"+songName+ext, fileLoc.songslist+"\\"+newName+ext
                print 'renaming to ', fileLoc.mysongs+"\\"+newName+ext
                os.rename(fileLoc.mysongs+"\\"+songName+ext, fileLoc.mysongs+"\\"+newName+ext)
            except:
                print 'file already created'
        else:
            'already fixed'
            
def compileSongs(sms,dr,flst):
    global mySongs
    print oldSongs
    mySongs = []
    print flst
    if len(oldSongs) == 0:
        soundController.queueSound(pygame.mixer.Sound(fileLoc.menuSounds+r"\menu_14_01.ogg"))
        soundController.playAllSounds()
    elif len(oldSongs) < len (flst):
        soundController.queueSound(pygame.mixer.Sound(fileLoc.menuSounds+r"\menu_14_02.ogg"))
        soundController.playAllSounds()
    for file in flst:
        songName = os.path.splitext(file.__str__())[0]
        print songName
            #you already have the info so skip it!
        if (oldSongs.count(songName) != 0):
            print 'Has it'
            mySongs.append ( (songName, "\\"+songName))
            oldSongs.remove(songName)
            continue
        else:
            print 'Does not have it',songName
            
        filename = fileLoc.mysongs+ "\\" + file.__str__()
        print currentDir
        ext = os.path.splitext(filename)[1]
        shutil.copy(filename,currentDir)
        newName = songName.replace(" ", "_")
        newName = newName.replace ("-","_")
        if (newName != songName):
            try:
                print currentDir
                print 'adding .',fileLoc.songslist+"\\"+songName+ext, fileLoc.songslist+"\\"+newName+ext
                os.rename(fileLoc.mysongs+"\\"+songName+ext, fileLoc.mysongs+"\\"+newName+ext)
            except:
                'file already created'
        songName = newName
        print songName
        #here you type in the song file without the extension
        
        if(ext == '.mp3'):
            print 'converting'
            os.system('Tag.exe --remove ' +songName+'.mp3')
            os.system("mp3towav.exe "+songName+".mp3 " +songName+".wav")
        os.system('aubiotrack.exe -O hfc -i '+songName+".wav >" +songName+ '.times') 
        shutil.move(fileLoc.singleplayer+songName+".mp3",fileLoc.songslist)
        #shutil.move(fileLoc.singleplayer+'\\'+songName+".wav",fileLoc.songslist)
        #shutil.remove(fileLoc.singleplayer+'\\'+songName+".wav")
        shutil.move(fileLoc.singleplayer+songName+".times",fileLoc.beats)
        mySongs.append ( (songName, "\\"+songName))
        
    for file in oldSongs:
        try:
            dddd=3
            os.remove(fileLoc.songslist+"\\"+file+".mp3")
            os.remove(fileLoc.beats+"\\"+file+".times")
        except:
            print "file already removed"
                    
            

class AubioCompiler(object):
    
    def loadSongs(self):
        sums = [0,0,1]
        #TODO: temp for "Wait while we compile your music
        os.path.walk(fileLoc.mysongs,changeNames,os.listdir(fileLoc.mysongs))
        os.path.walk(fileLoc.songslist,getOldSongs,os.listdir(fileLoc.songslist))
        os.path.walk(fileLoc.mysongs,compileSongs,os.listdir(fileLoc.mysongs))
        #print 'the test ', mySongs
        return mySongs

def loadSong():
   
    file = os.path.split(filename);

    print file[0]+'\n'
    print file[1]  # test
    
    #copies the song to the "Songs" directory
    #shutil.copy(filename,fileLocations.songs)
    shutil.copy(filename,fileLoc.singleplayer)
    #here you type in the song file without the extension
    
    songName = os.path.splitext(file[1])[0]
    print songName
    os.system('Tag.exe --remove ' +songName+'.mp3')
    os.system('mp3towav.exe '+songName+'.mp3 ' +songName+'.wav')
    os.system('aubiotrack.exe -O hfc -i '+songName+'.wav > '+songName+ '.times')
    shutil.copy(songName+".wav",fileLoc.songs)
    #shutil.move(file[0]+"\\"+songName+".times",fileLocations.beats)
    shutil.move(os.getcwd()+'\\'+songName+".times",fileLoc.beats)
    print 'end'
    return (songName, "\\"+songName)
    
"""
 #x = 3.924
currentBeat = 0

#while (x < 159):
    #print x
    #x += .495
timefile = "identity.times" 
diffs = [] 


times = [ float(t.strip()) for t in file(timefile, 'rt') ]
#tempTime = 1.230554
#for i in range(0,62):
    #tempTime = tempTime +.5258
    #print tempTime
    
    
for i in range(0,len(times) - 1):
    diffs.append(times[i] - times[i+1])
        
#for diff in diffs:
    #print diff


for i in range(3,len(diffs) - 4):
    #diffs.append(times[i] - times[i+1])
    diffs[i] = (diffs[i-3] + diffs[i-2] + diffs[i-1] + diffs[i] + diffs[i+1] + diffs[i+2] + diffs[i+3]) / 7
    print diffs[i]
currentNum = times[3]
print currentNum
for i in range(3,len(diffs) - 1):
    currentNum = currentNum -diffs[i]
    print currentNum
    
"""


"""
   File Locations holds all the base file locations needed in the program. This includes the following Directories
   SONGS
   BEATS
   SOUNDEFFECTS
   IMAGES -- added 10 March by jcisarano 
   IMAGES_MENUS -- added 26 March by jc
   MENUSOUND -- added 12 March by jc
   PlayerProfile -- added 16 March by jc
   Scores- added 15 April - Trey
"""

"""
   FileLocations started 22 Feb by Trey Brumley -- created file to return song, beat, and sound effect directories
"""
import os
import re
import sys
print sys.path, '123'
print 'sys arg',sys.argv
mydir = os.path.dirname(sys.argv[0])
print mydir, 'working with dir'
print os.getcwd(), 'this dir'
print os.path.abspath(mydir), 'abs dir'

remoteAccess = ''
if mydir:
    os.chdir(mydir)
else:
    basDirPattern=r"(.*\\)dist\\library.zip"
    regEx=re.compile(basDirPattern)
    matchedString=regEx.match(sys.path[0])
    tester = matchedString.group(1)+"src\\"
    remoteAccess = tester

class FileLocations(object):
    "Container for locations of important directories"
    global DIRFILE
    DIRFILE="FileLocationInfo.txt"
    def __init__ (self):
        """
            initilizes all of the directories needed.
        """
        if remoteAccess:
            workDir = tester
        else:
            workDir=os.getcwd()
        basDirPattern=r"(.*\\)src.*"
        songDirPattern=r"(.*\\)mtm\\src.*"
        regEx=re.compile(basDirPattern)
        regExSong=re.compile(songDirPattern)
        matchedString=regEx.match(workDir)
        if matchedString:
            baseDir=matchedString.group(1)
            songDir=regExSong.match(workDir).group(1)
        else:
            print 'base dir case'
            print workDir
            basDirPattern=r"(.*)\\dist"
            songDirPattern=r"(.*)\\mtm\\dist"
            regEx=re.compile(basDirPattern)
            regExSong=re.compile(songDirPattern)
            matchedString=regEx.match(workDir)
            if matchedString:
                baseDir=matchedString.group(1)+"\\"
                songDir=regExSong.match(workDir).group(1)+"\\"
                print baseDir, songDir
            else:
                print "ERROR LODING DIR1"
                print workDir
        #DIRECTORIES
        self.beats=baseDir+r"beats"
        self.images=baseDir+r"images"
        self.images_menus=baseDir+r"images\menus"
        self.menuSounds=baseDir+r"audio\menu"
        self.alphSounds=baseDir+r"audio\alphabet"
        self.nameEntry=baseDir+r"audio\name_entry"
        self.scoring=baseDir+r"audio\scoring"
        self.playerProfiles=baseDir+r"profiles"
        self.songs=baseDir+r"songs"
        self.songslist = baseDir +r"mysongs"
        self.numberSounds = baseDir+r"audio\numbers"
        self.soundEffects=baseDir+r"audio\fx"
        self.comboSounds = baseDir +r"audio\combos"
        self.stepSounds = baseDir +r"audio\steps"
        self.careerSounds = baseDir +r"audio\career"
        self.scores = baseDir +r"scores"
        self.singleplayer = baseDir+"src\\"
        self.mysongs = songDir +r"My Music"
        
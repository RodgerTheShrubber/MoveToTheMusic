"""
   High scores are added and saved. Player's high scores are stored for each song they have. Also,
   The song has a list of the top 5 players that have a High Score
"""

"""
   HighScores started 22 Feb by Trey Brumley -- created file to store top songs for each player.
"""
import os
import re
from FileLocations import FileLocations
import cPickle as pickle

class NameScore (object):
    test = "test"
    def __init__ (self,nam,val):
        self.value=val
        self.name=nam
        

class HighScores(object):
    "Container for locations of important directories"
    global DIRFILE
    DIRFILE="FileLocationInfo.txt"
    def __init__ (self):
        """
            initilizes all of the data needed.
        """
        self.top_song_scores = {}
        self.players_top_scores ={}
        self.newTopScore =False
        self.newPersonalScore = False
        
    def getSongScores(self):
        return self.top_song_scores
    def getPlayerSongScores(self):
        return self.players_top_scores
    def replaceScore(self,scoreDict,score,playerName):
        #assume there is not a new high score
        self.newTopScore =False
        index=0
        replace=0
        scoreList = scoreDict.keys()
        scoreList = sorted(scoreList)
        if(scoreDict.has_key(score)):
            return self.replaceScore(scoreDict,(int(score)+1),playerName)
            
        if(scoreList==None or score<scoreList[0]):
            if(scoreList==None or len(scoreList)<5):
                self.newTopScore =True
                scoreDict[score]=playerName
            return scoreDict
        
        if(scoreList!=None and len(scoreList)==5):
            del scoreDict[scoreList[0]]
        self.newTopScore =True
        scoreDict[score]= playerName
        
        return scoreDict 
    
    def updateHighScores(self,playerName,songName,score):
        if(self.top_song_scores.has_key(songName)):
            self.top_song_scores[songName]= self.replaceScore(self.top_song_scores[songName],int(score),playerName )
        else:
            self.top_song_scores[songName]= {int(score): playerName}
            self.newTopScore =True
            
            
    def replacePlayerScore(self,dict,score,playerName,songName):
        #assume there is not another high score
        self.newPersonalScore =False
        index=0
        replace=0
        
        scoreDict=dict[songName]
        scoreList = scoreDict.keys()
        scoreList = sorted(scoreList)
        if(scoreDict.has_key(score)):
           
            dict[songName]=self.replaceScore(scoreDict,(int(score)+1),playerName)
            self.newPersonalScore =True
            return dict
            
        if(scoreList==None or score<scoreList[0]):
            if(scoreList==None or len(scoreList)<5):
                self.newPersonalScore =True
                scoreDict[score]=playerName
            dict[songName]=scoreDict
            
            return dict
        
        if(scoreList!=None and len(scoreList)==5):
            del scoreDict[scoreList[0]]
        self.newPersonalScore =True
        scoreDict[score]= playerName
        
        dict[songName]=scoreDict
        
        return dict 
    
    def updatePlayerHighScores(self,playerName,songName,score):
        if(self.players_top_scores.has_key(playerName) and self.players_top_scores[playerName]!=None
        and self.players_top_scores[playerName].has_key(songName)):
            self.players_top_scores[playerName]= self.replacePlayerScore(self.players_top_scores[playerName],int(score),playerName,songName )
        else:
            if(self.players_top_scores.has_key(playerName) and self.players_top_scores[playerName]!=None):
                self.newPersonalScore =True
                self.players_top_scores[playerName].update({songName: { int(score): playerName} })
            else:
                self.newPersonalScore =True
                self.players_top_scores[playerName]= {songName: { int(score): playerName} }
            

    def loadSongScores(self):
        try:
            #filename handled internally -- derive it from playerName
            fileLocs=FileLocations()
            filename = fileLocs.songs+r"\songScores.p"
            f = open(filename, "r")
            tempIn = pickle.load(f)
            self.top_song_scores = tempIn.getSongScores()
            self.players_top_scores = tempIn.getPlayerSongScores()
            f.close()
            return True                       
        except IOError:
            self.top_song_scores = {}
            self.players_top_scores = {}
            return False
        except AttributeError:
            self.top_song_scores = {}
            self.players_top_scores = {}
        except EOFError:
            self.top_song_scores = {}
            self.players_top_scores = {}
    def saveSongScores(self):
        """
           Saves this profile to /profiles/gameprofile.p
           Only one profile is saved on a given machine. 
        """
        fileLocs=FileLocations()
        filename = fileLocs.songs+r"\songScores.p"
        try:
            f = open( filename, "w")
            pickle.dump(self, f)
            print 'High Scores Saved'
            return True
        except IOError:
            raise GameProfileIOError("Unable to write game profile to file.")
    
    def getScoresForSong(self,song):
        return reversed(sorted(self.top_song_scores[song]))
    def getScoresForPlayer(self,player,song):
        return reversed(sorted(self.players_top_scores[player][song]))
    
    def __revSortForSong(self,song):
        i=0
        j=0
        unsortList=self.top_song_scores[song]
        for list in unsortList:
            for comp in usortList:
                if (int(unsortList[j])<int(unsortList[i])):
                    temp = unsortList[i]
                    unsortList[i] =unsortList[j]
                    unsortList[j]= unsortList[i]
                j+=1
            i+=1
    def clearInfo(self):
        self = HighScores()
        self.saveSongScores()
    def printScores(self):
        for i in self.top_song_scores:
            for j in self.top_song_scores[i]:
                print i,self.top_song_scores[i][j],j
        for i in self.players_top_scores:
            for j in self.players_top_scores[i]:
                for k in self.players_top_scores[i][j]:
                    print i,j,k
        
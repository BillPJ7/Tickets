from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from .TicketsInfo import DataJobs
from random import *
import random

class Dummy:
    def MakeTestFile(OwnerID):
        people = DataJobs.GetPeopleTics(OwnerID)
        f = open('TestAppFile.txt', 'w')
        
        for pCnt, p in enumerate(people):
             
            for tCnt, t in enumerate(p):
                if tCnt == 0:
                    f.write('***\n') 
                else:
                    f.write(str(people[pCnt][tCnt]) + '\n')    
        f.close()
    def DummyGood(): # Test data for successful results
        DataJobs.AddTries(204, 5640) # Add 5640 tries to owner 204
        Best10 = Dummy.MakeBestTen()
        bCount = 0
        DataJobs.DeleteBestTen(204)
        for bCount, b in enumerate(Best10): # OwnerID, Diff, Bads, TenBestNbr
            DataJobs.AddBestTen(Best10[bCount][0], Best10[bCount][1], Best10[bCount][2], Best10[bCount][3])
        TenBest = Dummy.MakeTenBest()
        DataJobs.DeleteTenBest(204)
        for tCount, t in enumerate(TenBest): # PersonID, GameID, NumbTics, TenBestNbr
            DataJobs.AddTenBest(TenBest[tCount][0], TenBest[tCount][1], TenBest[tCount][2], TenBest[tCount][3])
        Status = Dummy.MakeStatus()
        DataJobs.DeleteStatus(204)
        for tCount, s in enumerate(Status): # PersonID, DupTeams, Bac2Bac, AvgRating, TenBestNbr
            DataJobs.AddStatus(Status[tCount][0], Status[tCount][1], Status[tCount][2], Status[tCount][3], Status[tCount][4])
    
    def DummyBad(): # Test data for unsuccessful result
        PersonMsg = DataJobs.CheckPersonMsg(459)
        DataJobs.NoResultEntry(231, PersonMsg)
        GameMsg = DataJobs.CheckGameMsg(5431)
        DataJobs.NoResultEntry(231, GameMsg)
        
    def MakeBestTen():
        Best10 = []
        Best10.append([204, 1.125, 0, 1]) # OwnerID, Diff, Bads, TenBestNbr
        Best10.append([204, 1.540, 0, 2])
        Best10.append([204, 1.826, 0, 3])
        Best10.append([204, 2.2, 0, 4])
        Best10.append([204, 2.44, 0, 5])
        Best10.append([204, 3.186, 0, 6])
        Best10.append([204, 4.8, 0, 7])
        Best10.append([204, 1.215, 1, 8])
        Best10.append([204, 2.34, 1, 9])
        Best10.append([204, 0.824, 2, 10])
        return Best10
    
    def MakeTenBest():
        TenBest = []
        People = [334,335,336,337,338,339]
        for b in range(1, 11):
            for p in People:
                for t in range(8):
                    GameID = Dummy.GetRandomGameID()
                    TenBest.append([p, GameID, randint(1, 4), b]) # PersonID, GameID, NumbTics, TenBestNbr
        return TenBest
        
    def GetRandomGameID():
        IDs = [5165,5178,5210,5230,5271,5282,5306,5352,5367,5383,5409,5431,5449,5467,5480,5497,5555,5574,5614,5658,5707,5714,5749,5762,5808,5826,5837,5847,5866,5884,6005,6025,6042,6068,6085,6119,6126,6194,6228,6251,6281]
        L = len(IDs)
        r = randint(0, L - 1)
        return IDs[r]
    
    def MakeStatus():#round(random.uniform(33.33, 66.66), 1)
        Status = []
        People = [334,335,336,337,338,339]
        for b in range(1, 11):
            for p in People:
                Status.append([p, randint(0, 1), randint(0, 1), round(random.uniform(10, 15), 5), b])
        return Status
                
    def PrintCombos(Combos):
        for c in Combos:
            print(c)
        print(str(len(Combos))) 
    
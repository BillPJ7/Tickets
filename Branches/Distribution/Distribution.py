from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from .TicketsInfo import DataJobs
from .Test import Dummy
import random
import time
import numpy as np

class Distribute:
    OwnerID = 0
    Combos = []
    Combo = []
    Person = []
    TicsPer = 0
    TlGames = 0
    TlPeople = 0
    Games = [] 
    GamesOrig = []
    PersonGame = []
    CurrentGame = 0
    Tries1 = 0
    TempResult = []
    
    def Run(OwnerID, Minutes):
        '''Must add feature to run with remaining tics during season'''
        Distribute.OwnerID = OwnerID
        O = DataJobs.GetOwnerByID(OwnerID)
        UserName = O.username
        Password = O.password
        if OwnerID == 204 and UserName == 'Al' and Password == 'g2':
            Dummy.DummyGood()
            return True
        if OwnerID == 231 and UserName == 'Al' and Password == 'i0':
            DataJobs.DeleteNoResultMessages(OwnerID)
            Dummy.DummyBad()
            return False
        Distribute.TicsPer = DataJobs.GetTicsPer(OwnerID)
        Distribute.TlGames = DataJobs.GetGameCount(OwnerID)
        Distribute.TlPeople = DataJobs.GetPersonCount(OwnerID)
        Distribute.Person = DataJobs.GetPersonArray(Distribute.OwnerID)
        Distribute.Games = DataJobs.GetGameArray(OwnerID)
        Distribute.GamesOrig = DataJobs.GetGameArray(OwnerID)
        Distribute.PersonGame = DataJobs.GetPersonGame(Distribute.OwnerID)
        
        Tries = DataJobs.GetTries(OwnerID)
        Distribute.Tries1 = 0
        GoodTries = 0
        DataJobs.DeleteNoResultMessages(Distribute.OwnerID)
        MaxTime = Minutes * 60 # seconds
        StartTime = time.time()
        while (time.time() - StartTime) < MaxTime:
            if Distribute.Attempt():
                Distribute.UseCombos()
                GoodTries += 1
            #else:
                #return False
            Tries += 1
            Distribute.Tries1 += 1
            #if Tries > 10:
              #  break
            Distribute.ResetPersonArray()
        print('Tries = ' + str(Tries))
        print('GoodTries = ' + str(GoodTries))
      #  Dummy.PrintCombos(Distribute.Combos)
        DataJobs.AddTries(OwnerID, Tries)
        Best10Cnt = len(DataJobs.GetBestTen(OwnerID))
        print(str(Best10Cnt)+'#################################')#was 2 when expected 0
        if Tries == 0 or Best10Cnt == 0:
            return False 
        return True

    def Attempt():
        Distribute.Combos = []
        print('TlGames is ' + str(Distribute.TlGames))
        Distribute.TempResult = []
        for p in range(Distribute.TlPeople):
            TempPerson = []
            for g in range(Distribute.TlGames):
                TempPerson.append(0)
            Distribute.TempResult.append(TempPerson)
        random.shuffle(Distribute.Games)
        for gCnt, g in enumerate(Distribute.Games):
            g['GameNbr'] = gCnt
        if Distribute.DoCombos('Run'):
            for r in filter(Distribute.ReqsOnly, Distribute.Games):
                Distribute.CurrentGame = c = r['GameNbr']
                #print(r)
                if not Distribute.ComboFits(r, Distribute.Combos[c]):
                    Found = False
                    for g in filter(Distribute.GamesNotThis, Distribute.Games):
                        n = g['GameNbr']
                        if Distribute.ComboFits(g, Distribute.Combos[c]) and Distribute.ComboFits(r, Distribute.Combos[n]):
                            Distribute.SwapCombos(c, n)
                            Found = True
                            break
                    if Found == False:
                        return False
            return True
        return False

    def DoCombos(From):
        print('hey wtf')
        for t in range(Distribute.TicsPer, 1, -1):
            Distribute.GetCombos(t, Distribute.TicsPer)
        print('TlGames is ' + str(Distribute.TlGames))
        print('combos len is ' + str(len(Distribute.Combos)))
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
        CauseInfo = ''
        if From == 'People':
            CauseInfo = 'No results found after People entry'
        elif From == 'Requirements':
            CauseInfo = 'No results found after Requirements entry'
        DataJobs.NoResultEntry(Distribute.OwnerID, CauseInfo)
        return False
    
    def GetCombos(Tics, TicsPer):
        while True:
            ColCount = 0
            Distribute.Combo = []
            g = len(Distribute.Combos) - 1
           # if g > 40:
              #  g = 40
            #if g > 16:
                #g = 16
            print('g is ' + str(g))
            GameNbrOrig = Distribute.Games[g]['GameNbrOrig']
            for p in range(Distribute.TlPeople):
                Dict = {
                    "Tics": 0,
                    "GameID": Distribute.Games[g]['GameID'],
                    "GameNbrOrig": Distribute.Games[g]['GameNbrOrig'], # before the shuffle
                    "GameNbr": Distribute.Games[g]['GameNbr'],
                    "GameDate": Distribute.Games[g]['GameDate'],
                    "TeamID": Distribute.Games[g]['TeamID'],
                    "Rating": Distribute.Games[g]['Rating']
                }
                Distribute.Combo.append(Dict)
            p = Distribute.AssignIt(Tics, -1)
            if p > -1:
                Distribute.Combo[p]['Tics'] = Tics
                print('len of TempResult[p] is ' + str(len(Distribute.TempResult[p])))
                print('GameNbrOrig is ' + str(GameNbrOrig))
                Distribute.TempResult[p][GameNbrOrig] = Tics
                ColCount += Tics
                if ColCount < TicsPer:
                    for t in range(TicsPer - ColCount, 0, -1):
                        if ColCount + t <= TicsPer:
                            p = Distribute.AssignIt(t, p)
                            if p > -1:
                                Distribute.Combo[p]['Tics'] = t
                                Distribute.TempResult[p][GameNbrOrig] = t
                                ColCount += t
                                if ColCount == TicsPer:
                                    break
                if ColCount == TicsPer:
                    Distribute.Combos.append(Distribute.Combo)
            else: break

    def ResetPersonArray():
        for p in Distribute.Person:
            for t in p:
                t['Tics'] = t['StartTics']
                t['Left'] = t['StartLeft']
                            
    def AssignIt(Tics, MatchingWith): 
        high = 0 
        UseP = -1
        UseT = -1
        PeopTics = []
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt == MatchingWith: continue # don't give someone 2 sets of tickets on the same day
            for tCnt, t in enumerate(p):
                if t['Tics'] == Tics and t['Left'] > 0:
                    if t['Left'] >= high:
                        if t['Left'] > high:
                            PeopTics = []
                            high = t['Left']
                        Dict = {
                            "Person": pCnt,
                            "UseT": tCnt,
                            "Tics": t['Tics']
                        }
                        PeopTics.append(Dict)
        if len(PeopTics) > 0:
            p = Distribute.GetP(PeopTics)
            UseP = PeopTics[p]['Person']
            UseT = PeopTics[p]['UseT']
            Distribute.Person[UseP][UseT]['Left'] -= 1
        return UseP
    
    def GetP(PeopTics):
        #use len(Combos) to know what combo you're on, and find out what game to check others
       # return 0
        i = len(PeopTics) - 1
        return random.randint(0, i)
        if len(PeopTics) == 1:
            return 0
        else:
            Low = 4
            pScores = []
            for pCnt, p in enumerate(PeopTics):
                pScores.append(3)
                TempCombo = []
                L = len(Distribute.Combos)
                TestTicCnt = 0
                for c in Distribute.Combo:
                    Dict = {
                        "Tics": c['Tics'],#Distribute.Combos[L - 1][pCnt]['Tics'],
                        "GameID": c['GameID']#Distribute.Combos[L - 1][pCnt]['GameID'] 
                    }
                    TestTicCnt += c['Tics']
                    TempCombo.append(Dict)
              #  if Distribute.Tries1 == 0 and TestTicCnt != 4:
                  #  print('TicCnt is not 4')
               # TempCombo[p['Person']]['Tics'] = p['Tics']
                TempCombo[p['Person']]['Tics'] = p['Tics']
                if not(Distribute.FitsReq(Distribute.Games[L], TempCombo)):
                    pScores[pCnt] = 3
                    if 3 < Low:
                        Low = 3                    
                else:
                    Bads = Distribute.GetBads(PeopTics, pCnt)
                    #if Distribute.Tries1 == 0:
                     #   print('pCnt is ' + str(pCnt))
                     #   print('Bads is ' + str(Bads))
                    pScores[pCnt] = Bads
                    if Bads < Low:
                        Low = Bads
            if Low > 2:
              #  if Distribute.Tries1 == 0:
              #  print(TempCombo)
              #  for cCount, c in enumerate(TempCombo):
                 #   print(Distribute.Games[L]['Person'][cCount])
                return 0
            else:
                Lows = []
                for pCnt, p in enumerate(PeopTics):
                    if pScores[pCnt] == Low:
                        Lows.append(pCnt)
                if len(Lows) > 1:
                    return Distribute.GetBestAverage(PeopTics, Lows)
                else:
                    return Lows[0]
    
    def GetBads(PeopTics, pCnt):
        #return 0
        p = PeopTics[pCnt]
        Bads = 0
        L = len(Distribute.Combos)
        GameNbrOrig = Distribute.Games[L]['GameNbrOrig'] 
        if GameNbrOrig > 0:
            if Distribute.TempResult[pCnt][GameNbrOrig - 1] > 0:
                GameDate = Distribute.GamesOrig[GameNbrOrig]['GameDate']
                PrevGameDate = Distribute.GamesOrig[GameNbrOrig - 1]['GameDate']
                if DataJobs.AreBackToBack(Distribute.OwnerID, GameDate, PrevGameDate):
                    Bads += 1
                    if Distribute.Tries1 == 0:
                        print('Person ' + str(pCnt))
                        print(GameDate)
                        print(PrevGameDate)
        return Bads
        '''
        GameDate = Distribute.Games[L]['GameDate']
        Team = Distribute.Games[L]['TeamID'] 
        GameNbrOrig = Distribute.Games[L]['GameNbrOrig'] 
        if GameNbrOrig > 0:
            CompareGameNbr = Combos[GameNbrOrig - 1]
            print()
              
        for c in Distribute.Combos:
            if c[pCnt]['Tics'] > 0:
                CompareDate = c[pCnt]['GameDate']
                if GameDate > CompareDate:
                    if DataJobs.AreBackToBack(Distribute.OwnerID, GameDate, CompareDate):
                        if Distribute.Tries1 == 0:
                            print(GameDate)
                            print(CompareDate)
                      #  Bads += 1
                      #  if Bads == 2:
                      #      return 2
                CompareTeam = c[pCnt]['TeamID']
                if Team == CompareTeam:
                    if Distribute.Tries1 == 0:
                        print(str(Team))
                    Bads += 1
                    if Bads == 2:
                        return 2
                        
        return Bads
    '''
    
    def GetBestAverage(PeopTics, Lows):
        return 0    
      
    def UpdatePersonGame():
        for p in Distribute.PersonGame:
            p[1] = []
        for cCnt, c in enumerate(Distribute.Combos):
            for pCnt, p in enumerate(c):
                Tics = Distribute.Combos[cCnt][pCnt]['Tics']
                if Tics > 0:
                    Dict = {
                        "Tics": Tics,
                        "GameID": Distribute.Games[cCnt]['GameID'],
                        "TeamID": Distribute.Games[cCnt]['TeamID'],
                        "GameDate": Distribute.Games[cCnt]['GameDate'],
                        "TeamRating": Distribute.Games[cCnt]['Rating'],
                    }
                    Distribute.PersonGame[pCnt][1].append(Dict)

    def UseCombos():
        Status = []
        Distribute.UpdatePersonGame()
        for pCnt, p in enumerate(Distribute.PersonGame):
            Teams = []
            BackToBacks = 0
            RatingCount = 0
            L = len(p[1])
            Dates = []
            for gCount, g in enumerate(p[1]):
                Teams.append(g['TeamID'])
                RatingCount += g['TeamRating'] * g['Tics']
                Dates.append(g['GameDate'])
            Dates = np.array(Dates)
            Dates = np.sort(Dates)
            for dCnt, d in enumerate(Dates):
                if dCnt > 0:
                    if DataJobs.AreBackToBack(Distribute.OwnerID, d, PrevDate):
                        BackToBacks += 1
                PrevDate = d
            Dict = {
                "PersonID": p[0],
                "Dups": len(Teams) - len(set(Teams)),
                "BackToBacks": BackToBacks,
                "AverageRating": RatingCount / DataJobs.GetPersonTlTics(p[0])
            }        
            Status.append(Dict)  
        Result = Distribute.CompareToBest(Status)
        TenBestNbr = Result[2]
        TlBestTen = DataJobs.GetBestTenCount(Distribute.OwnerID)
        if TenBestNbr > 0:
            Distribute.InsertBestTen(Result[0], Result[1], TenBestNbr, TlBestTen)
            if Distribute.Tries1 == 0:
                print(Status)
            Distribute.InsertStatus(Status, TenBestNbr, TlBestTen)
            Distribute.InsertTenBest(Distribute.PersonGame, TenBestNbr, TlBestTen)

    def InsertBestTen(Diff, Bads, TenBestNbr, TlBestTen):
        if TenBestNbr == 10:
            DataJobs.Update10thBestTen(Distribute.OwnerID, Diff, Bads)
        else:
            DataJobs.BumpBestTen(Distribute.OwnerID, Diff, Bads, TenBestNbr, TlBestTen)
        
    def InsertStatus(Status, TenBestNbr, TlBestTen):
        if TenBestNbr == 10:
            for p in Status:
                DataJobs.Update10thStatus(p['PersonID'], p['Dups'], p['BackToBacks'], p['AverageRating'])
        else:
            for p in Status:
                DataJobs.BumpStatus(p['PersonID'], p['Dups'], p['BackToBacks'], p['AverageRating'], TenBestNbr, TlBestTen)
                
    def InsertTenBest(PersonGame, TenBestNbr, TlBestTen):
        if TenBestNbr <= 10:
            DataJobs.BumpTenBest(Distribute.OwnerID, TenBestNbr, TlBestTen)
        for p in PersonGame:
            PersonID = p[0]
          #  print('*********PersonID is ' + str(PersonID))
            for g in p[1]:
               # print('GameID is ' + str(g['GameID']))
                DataJobs.AddTenBest(PersonID, g['GameID'], g['Tics'], TenBestNbr)
    
    def CompareToBest(Status):
        Low = 100
        Hi = 0
        Bads = 0
        TenBestNbr = 0
        for s in Status:
            if s['AverageRating'] < Low:
                Low = s['AverageRating']
            if s['AverageRating'] > Hi:
                Hi = s['AverageRating']
            Bads += s['Dups'] + s['BackToBacks']
        Diff = Hi - Low
        B = DataJobs.GetBest(Distribute.OwnerID)
        if B.count() == 0:
            return [Diff, Bads, 1]
        Found = False
        for bCount, b in enumerate(B):
            if (Bads < b.bads) or (Bads == b.bads and Diff < b.difference):
                TenBestNbr = bCount + 1
                Found = True
                break
        if Found == False:
            if B.count() < 10:
                TenBestNbr = B.count() + 1
        return [Diff, Bads, TenBestNbr]
    
    def ReqsOnly(Games):
        if Games['ReqGame'] == True:
            return True
        return False
        
    def GamesNotThis(Games):
        if Games['GameNbr'] == Distribute.CurrentGame:
            return False
        return True

    def FitsReq(Game, Combo):
        if Game['ReqGame'] == False:
            return True
        ReqCnt = 0
        ComboCnt = 0
        '''
This could be a partially filled combo, so if tickets go on a no req person,
it only doesn't fit if the reqs plus the tickets > TicsPer
        '''
        PrintIt = False
        Tic2 = 0
        for cCount, c in enumerate(Combo):
            Tics = c['Tics']
            if Tics == 4:
                break
            if Tics == 2:
                Tic2 += 1
        for cCount, c in enumerate(Combo):
            Req = Game['Person'][cCount]
            Tics = c['Tics'] 
            if Req == 0 and Tics > 0: # trying to put tics on a can't see game
                return False
            if Req == None and Tics > 0:
                ComboCnt += Tics
            elif Req != None:
                if Req > 0 and Tics == 0:
                    ReqCnt += Req
        if ReqCnt + ComboCnt > Distribute.TicsPer:
            return False
        return True    
              
    def ComboFits(Game, Combo):
        if Game['ReqGame'] == False:
            return True
        for cCount, c in enumerate(Combo):
            Req = Game['Person'][cCount]
            print('Req is ' + str(Req))
            print('c[Tics] is ' + str(c['Tics']))
            if Req != c['Tics'] and Req != None:
                return False
        return True

    def SwapCombos(GameNbr1, GameNbr2):
        TempCombo = Distribute.Combos[GameNbr1]
        Distribute.Combos[GameNbr1] = Distribute.Combos[GameNbr2]
        Distribute.Combos[GameNbr2] = TempCombo

        
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
    useT = -1
    useP = -1
    useP2 = -1
    def Run(OwnerID, Minutes):
        '''Must add feature to run with remaining tics during season'''
        '''
        i = 0
        StartTime = time.time()
        while (time.time() - StartTime) < 60:    
            i += 1
        print('loop ' + str(i))
        return False
    '''
    
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
        MaxTime = Minutes * 10 # seconds
        StartTime = time.time()
        while (time.time() - StartTime) < MaxTime:
         #   print(str(time.time() - StartTime))
            if Distribute.Attempt(OwnerID) == False:
             #   print('got here3')
                return False
            
            #return True ############################################            
            
            """
            if Distribute.Attempt():
                Distribute.UseCombos()
                GoodTries += 1
            for gCnt, g in enumerate(Distribute.Combos):
                s = ''
                for pCnt in range(Distribute.TlPeople):
                    s += str(Distribute.Combos[gCnt][pCnt]['Tics']) + ' '
                print(s)
            print(str(len(Distribute.Combos)))
            Tries += 1
            Distribute.Tries1 += 1

            Distribute.ResetPersonArray()
         """   
       # return True ######################## comment this, only runs once
        
        
        
        print('Tries = ' + str(Tries))
        print('GoodTries = ' + str(GoodTries))
      #  Dummy.PrintCombos(Distribute.Combos)
      #  DataJobs.AddTries(OwnerID, Tries)
        Best10Cnt = len(DataJobs.GetBestTen(OwnerID))
        #if Tries == 0 or Best10Cnt == 0:
          #  return False 
        return True

    def Attempt(OwnerID):
      #  print('mark1')
        Distribute.Combos = []
        Distribute.TempResult = []
      #  print('mark2')
        for p in range(Distribute.TlPeople):
        #    print('mark3')
            TempPerson = []
            for g in range(Distribute.TlGames):
           #     print('mark4')
                TempPerson.append(0)
            #    print('mark5')
         #   print('mark6')
            Distribute.TempResult.append(TempPerson)
           # print('mark7')
       # random.shuffle(Distribute.Games)
      #  for gCnt, g in enumerate(Distribute.Games):
        #    g['GameNbr'] = gCnt
        
        Tries = DataJobs.GetTries(OwnerID)
        Distribute.Tries1 = 0
        GoodTries = 0
     #   print('mark8')
        
        if Distribute.DoCombos('Run'):
         #   print('wtf')
            tlTries = 0
            while tlTries < 10:
             #   print('got here')
                random.shuffle(Distribute.Games)
                for gCnt, g in enumerate(Distribute.Games):
                    g['GameNbr'] = gCnt
                for r in filter(Distribute.ReqsOnly, Distribute.Games):
                    Distribute.CurrentGame = c = r['GameNbr']
                    if not Distribute.ComboFits(r, Distribute.Combos[c]):
                        Found = False
                        for g in filter(Distribute.GamesNotThis, Distribute.Games):
                            n = g['GameNbr']
                            if Distribute.ComboFits(g, Distribute.Combos[c]) and Distribute.ComboFits(r, Distribute.Combos[n]):
                                Distribute.SwapCombos(c, n)
                                Found = True
                                break
                        if Found == False:
                            #return False
                            print('bad')
                #return True
                #print('good')
                tlTries +=1
                
                Distribute.UseCombos()
                GoodTries += 1
                Tries += 1
                Distribute.Tries1 += 1
    
                Distribute.ResetPersonArray()
            print('Tries='+str(Tries))
            DataJobs.AddTries(OwnerID, Tries)    
                
        return True        
        #return False
    
    def DoCombos(From):
        Distribute.AllTics()
       # print('combo len is ' + str(len(Distribute.Combos)))
      #  print('total games is' + str(Distribute.TlGames))
    #    print('dc1')
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
        
    #    print('dc2')
        if Distribute.AllMinus1() == False:
            return False
     #   print('dc3')
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
      #  print('dc4')
        if Distribute.HalfTics() == False:
            print('ht')
            return False
     #   print('dc5')
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
    #    print('dc6')
        if Distribute.TicsPer == 2: # Done, didn't work
            return False
    #    print('dc7')
        if Distribute.AllMinus2() == False:
            return False
     #   print('dc8')
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
    #    print('dc9')
        if Distribute.Twos() == False:
            return False
    #    print('len of Combos is'+str(len(Distribute.Combos)))
        if len(Distribute.Combos) == Distribute.TlGames:
      #      print('yeah')
            return True
        """
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
        Distribute.AllMinus3()
        if len(Distribute.Combos) == Distribute.TlGames:
            return True
        """
        return False
    
    def Twos():
        while True:
            if Distribute.AllTwos() == True:
                Distribute.StartCombo()
                useP3 = Distribute.Get2(-1, -1, -1)
              #  print(str(useP3))
                Distribute.AssignIt(2, useP3, Distribute.useT)
                useP2 = Distribute.Get2(useP3, -1, -1)
                Distribute.AssignIt(2, useP2, Distribute.useT)
                useP = Distribute.Get2(useP3, useP2, -1)
                Distribute.AssignIt(2, useP, Distribute.useT)
                Distribute.Combos.append(Distribute.Combo)
            else:
                return True
    
    def Get2(skipP, skipP2, skipP3):
        hiTwos = 0
        useP = -1
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt != skipP and pCnt != skipP2 and pCnt != skipP3:
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 2 and Distribute.GorGE(t['Left'], hiTwos):
                  #  if t['Tics'] == 2 and t['Left'] >= hiTwos: # = would be tie...
                        useP = pCnt
                        hiTwos = t['Left']
                        Distribute.useT = tCnt
                        continue
        return useP
    
    def GorGE(a, b):
        r = random.randint(0, 1)
        if r == 0:
            if a >= b:
                return True
            else: return False
        else:
            if a > b:
                return True
            else: return False
            
    def AllTwos():
        if Distribute.TicsPer % 2 != 0:
            return False
        twoCount = 0
        twos = int(Distribute.TicsPer / 2)
        for pCnt, p in enumerate(Distribute.Person):
            for tCnt, t in enumerate(p):
                if t['Tics'] == 2 and t['Left'] > 0:  
                    twoCount += 1
                   # print('twoCount=' + str(twoCount))
                   # print('twos=' + str(twos))
                    if twoCount == twos:
                        return True
        return False 
    
    def AllTics():
        for pCnt, p in enumerate(Distribute.Person):
            for tCnt, t in enumerate(p):
                if t['Tics'] == Distribute.TicsPer:
                    while t['Left'] > 0:
                        Distribute.StartCombo()
                        Distribute.AssignIt(t['Tics'], pCnt, tCnt)
                        Distribute.Combos.append(Distribute.Combo)
                        
    def HalfTics():

        if Distribute.TicsPer % 2 != 0:
            return True
        ticPer = int(Distribute.TicsPer / 2)
        if ticPer == 2:
            return True
       # test = 0
        while True:
            useP = -1
            useP2 = -1
            useT = -1
            useT2 = -1
            hiTP = 0
            for pCnt, p in enumerate(Distribute.Person):
                for tCnt, t in enumerate(p):
                    if t['Tics'] == ticPer and t['Left'] > 0 and Distribute.GorGE(t['Left'], hiTP):
                   # if t['Tics'] == ticPer and t['Left'] > 0 and t['Left'] >= hiTP: # = would be tie...
                       # if test >= 2:
                           # print('pCnt=' + str(pCnt))
                           # print('tLeft=' + str(t['Left']))
                        if useP2 > -1:
                            useP = useP2
                            useP2 = pCnt
                            useT = useT2
                            useT2 = tCnt
                        elif useP > -1:
                            useP2 = pCnt
                            useT2 = tCnt
                        else:
                            useP = pCnt
                            useT = tCnt
                        hiTP = t['Left']
            #if test == 2:
               # print('here1')
            if useP2 > -1:
              #  print('here2')
                Distribute.StartCombo()
                Distribute.AssignIt(ticPer, useP, useT)
                Distribute.AssignIt(ticPer, useP2, useT2)
                Distribute.Combos.append(Distribute.Combo)
            elif useP > -1:
              #  print('here3')
                if ticPer == 2:
                    if Distribute.TwoOnes(useP) == True:
                        useP2 = Distribute.Get1(useP, -1, -1)
                        Distribute.StartCombo()
                        Distribute.AssignIt(1, useP2, 0)
                        useP = Distribute.Get1(useP, useP2, -1)
                        Distribute.AssignIt(1, useP, 0)
                        Distribute.Combos.append(Distribute.Combo)
                    else:
                        return False
                elif ticPer == 3:
                    if Distribute.Ones(useP, 3) == True:
                        
                        useP3 = Distribute.Get1(useP, -1, -1)
                        Distribute.StartCombo()
                        Distribute.AssignIt(3, useP, useT)
                     #   print('useP3=' + str(useP3))
                        Distribute.AssignIt(1, useP3, Distribute.useT)
                        useP2 = Distribute.Get1(useP, useP3, -1)
                     #   print('useP2=' + str(useP2))
                        Distribute.AssignIt(1, useP2, Distribute.useT)
                        useP = Distribute.Get1(useP, useP3, useP2)
                     #   print('useP=' + str(useP))
                        Distribute.AssignIt(1, useP, Distribute.useT)
                        Distribute.Combos.append(Distribute.Combo)
                        
                    elif Distribute.TwoOne(useP) == True:
                        useP2 = Distribute.GetGood2(useP)
                        Distribute.StartCombo()
                        Distribute.AssignIt(3, useP, useT)
                        Distribute.AssignIt(2, useP2, Distribute.useT)
                        useP = Distribute.Get1(useP, useP2, -1)
                        Distribute.AssignIt(1, useP, 0)
                        Distribute.Combos.append(Distribute.Combo)
                    else:
                        return False
            else:
                return True
        return True
    
    def Ones(skipP, oneCnt):
        oneCount = 0
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt != skipP:
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 1 and t['Left'] > 0:  
                        oneCount += 1
                        if oneCount == oneCnt:
                            return True
        return False 
    
    def TwoOne(skipP):
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt != skipP:
                
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 2 and t['Left'] > 0:
                        Distribute.useP = pCnt
                        for pCnt2, p2 in enumerate(Distribute.Person):
                            if pCnt2 != skipP and pCnt2 != pCnt:
                                for tCnt2, t2 in enumerate(p2):
                                    if t2['Tics'] == 1:
                                        if t2['Left'] > 0:
                                            Distribute.useP2 = pCnt2
                                            return True
                                    else:
                                        continue
        return False
    
    def Get1(skipP, skipP2, skipP3):
        hiOnes = 0
        useP = -1
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt != skipP and pCnt != skipP2 and pCnt != skipP3:
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 1 and t['Left'] > 0 and Distribute.GorGE(t['Left'], hiOnes):
                   # if t['Tics'] == 1 and t['Left'] >= hiOnes: # = would be tie...
                        useP = pCnt
                        hiOnes = t['Left']
                        Distribute.useT = tCnt
                        continue
        return useP
                        
    def AllMinus1():
        ticPer = Distribute.TicsPer - 1
        if ticPer == 1: # 2 TicsPer
            while True:
                useP = -1
                useP2 = -1
                Distribute.StartCombo()
                useP = Distribute.Get1(-1, -1, -1)
           #     print('useP is '+str(useP))
                if useP == -1:
                    return True
                Distribute.AssignIt(1, useP, 0)
                useP2 = Distribute.Get1(useP, -1, -1)
          #      print('useP2 is '+str(useP2))
                Distribute.AssignIt(1, useP2, 0)
                Distribute.Combos.append(Distribute.Combo)
        if ticPer == 2: # 3 TicsPer
            Ones = 0
            Two1s = 0            
            while True:

                if Distribute.Ones(-1, 3) == True:
                    Distribute.StartCombo()
                    useP = Distribute.Get1(-1, -1, -1)
                    Distribute.AssignIt(1, useP, 0)
                    useP2 = Distribute.Get1(useP, -1, -1)
                    Distribute.AssignIt(1, useP2, 0)
                    useP3 = Distribute.Get1(useP, useP2, -1)
                    Distribute.AssignIt(1, useP3, 0)
                    Distribute.Combos.append(Distribute.Combo)
                    Ones += 1
                #    print('Ones = ' + str(Ones))
                elif Distribute.TwoOne(-1) == True:
                   # useP = Distribute.GetGood2(-1)
                    useP = Distribute.useP
                    if useP == -1:
                        print('fuck1')
                    if len(Distribute.Combos) == Distribute.TlGames:
                        return True
                    Distribute.StartCombo()
                    Distribute.AssignIt(2, useP, Distribute.useT)
                   # Distribute.AssignIt(2, useP2, Distribute.useT)
                   # useP = Distribute.Get1(useP, -1, -1)
                    useP = Distribute.useP2
                    if useP == -1:
                        print('fuckyou')
                    Distribute.AssignIt(1, useP, 0)
                    Distribute.Combos.append(Distribute.Combo)
                    if len(Distribute.Combos) == Distribute.TlGames:
                        return True
                    Two1s += 1
                  #  print('Two1s = ' + str(Two1s))
                else:
                    return True
                
            return True
                
                    
        while True:
            hiTP = 0
            hiOnes = 0
            useP = -1
            useT = -1
            for pCnt, p in enumerate(Distribute.Person):
                currOnes = 0
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 1:
                        currOnes = t['Left']
                    elif t['Tics'] == ticPer:
                        if t['Left'] > 0:
                            if t['Left'] > hiTP:
                                hiTP = t['Left']
                                hiOnes = currOnes
                                useP = pCnt
                                useT = tCnt
                            elif t['Left'] == hiTP:
                                if Distribute.GorGE(currOnes, hiOnes):
                               # if currOnes >= hiOnes: # = would be tie, should choose (to do)
                                    hiOnes = currOnes
                                    useP = pCnt
            
            if hiTP > 0:
                Distribute.StartCombo()
                Distribute.AssignIt(ticPer, useP, useT) 
                useP = Distribute.GetGood1(useP, -1, -1, ticPer)
                if useP == -1:
                    return False
                Distribute.AssignIt(1, useP, 0)
                Distribute.Combos.append(Distribute.Combo)
            if useP == -1:
                return True
        return True 
    
    def AllMinus2():
        ticPer = Distribute.TicsPer - 2
        while True:
            hiTP = 0
            hiOnes = 0
            useP = -1
            useT = -1
            for pCnt, p in enumerate(Distribute.Person):
                currOnes = 0
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 1:
                        currOnes = t['Left']
                    elif t['Tics'] == ticPer:
                        if t['Left'] > 0:
                            if t['Left'] > hiTP:
                                hiTP = t['Left']
                                hiOnes = currOnes
                                useP = pCnt
                                useT = tCnt
                            elif t['Left'] == hiTP:
                                if Distribute.GorGE(currOnes, hiOnes) and currOnes > 0:
                              #  if currOnes >= hiOnes and currOnes > 0: # = would be tie, should choose (to do)
                                    hiOnes = currOnes
                                    useP = pCnt
            
            if hiTP > 0:
                Distribute.StartCombo()
                Distribute.AssignIt(ticPer, useP, useT) 
                if Distribute.Ones(useP, 2) == True:
                    useP2 = Distribute.GetGood1(useP, -1, -1, ticPer)
                    Distribute.AssignIt(1, useP2, 0)
                    useP = Distribute.GetGood1(useP, useP2, -1, ticPer)
                    Distribute.AssignIt(1, useP, 0)
                    Distribute.Combos.append(Distribute.Combo)
                else:
                    useP = Distribute.GetGood2(useP)
                    if useP == -1:
                        return False
                    
                 #   print('Before')
                  #  print('useP =' + str(useP))
                 #   print('useT =' + str(Distribute.useT))
                    Distribute.AssignIt(2, useP, Distribute.useT)
                  #  print('After')
                    Distribute.Combos.append(Distribute.Combo)
            if useP == -1:
                return True
        return True 
    
    def GetGood1(skipP, skipP2, skipP3, ticPer):  
        hiOnes = 0 
        hiTicPer = 0  
        useP = -1 
        checkTie = False
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt != skipP and pCnt != skipP2 and pCnt != skipP3:
                onT = False
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 1:
                        if t['Left'] >= hiOnes:
                            onT = True
                            if t['Left'] > hiOnes:
                                useP = pCnt
                            hiOnes = t['Left']
                            checkTie = True
                    elif t['Tics'] == ticPer and checkTie == True and onT == True:
                        if t['Left'] > 0 and Distribute.GorGE(t['Left'], hiTicPer):
                      #  if t['Left'] > 0 and t['Left'] >= hiTicPer: # = would be tie, should choose (to do)
                            if t['Left'] == 0:
                                print('dumbass')
                            useP = pCnt
                            hiTicPer = t['Left']
        return useP
    
    def GetGood2(skipP):
        hi2 = 0
        useP = -1
        for pCnt, p in enumerate(Distribute.Person):
            if pCnt != skipP:
                for tCnt, t in enumerate(p):
                    if t['Tics'] == 2:
                        if t['Left'] > 0 and Distribute.GorGE(t['Left'], hi2):
                       # if t['Left'] > 0 and t['Left'] >= hi2: # = would be tie, should choose (to do)
                            useP = pCnt
                            Distribute.useT = tCnt
                            hi2 = t['Left']
        return useP
                            
        
    
    def AssignIt(Tics, p, t):
        Distribute.Combo[p]['Tics'] = Tics
        Distribute.Person[p][t]['Left'] -= 1
      
    """                            
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
"""
    def StartCombo():
        ColCount = 0
        Distribute.Combo = []
        g = len(Distribute.Combos) - 1 
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
        

    def ResetPersonArray():
        for p in Distribute.Person:
            for t in p:
                t['Tics'] = t['StartTics']
                t['Left'] = t['StartLeft']

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
                TempCombo[p['Person']]['Tics'] = p['Tics']
                if not(Distribute.FitsReq(Distribute.Games[L], TempCombo)):
                    pScores[pCnt] = 3
                    if 3 < Low:
                        Low = 3                    
                else:
                    Bads = Distribute.GetBads(PeopTics, pCnt)
                    pScores[pCnt] = Bads
                    if Bads < Low:
                        Low = Bads
            if Low > 2:
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
        return Bads
    
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
            for g in p[1]:
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
            if Req != c['Tics'] and Req != None:
                return False
        return True

    def SwapCombos(GameNbr1, GameNbr2):
        TempCombo = Distribute.Combos[GameNbr1]
        Distribute.Combos[GameNbr1] = Distribute.Combos[GameNbr2]
        Distribute.Combos[GameNbr2] = TempCombo

"""
    def DoCombos(From):
        for t in range(Distribute.TicsPer, 1, -1):
            Distribute.GetCombos(t, Distribute.TicsPer)
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
"""
"""                            
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
"""
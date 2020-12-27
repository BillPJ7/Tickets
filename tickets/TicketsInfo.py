from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Owner, League, Team, Schedule, Person, Ticket, Req, BestTen, TenBest, Status, NoResult
from django.db.models import Q
from django.conf import settings
from decimal import Decimal

class DataJobs:
    def GetOwner(UserName, Password): 
        return Owner.objects.filter(username=UserName, password=Password)
    
    def GetOwnerByID(OwnerID):
        return Owner.objects.get(id=OwnerID)
    
    def AddInitialOwner(UserName, Password): #Before team and tickets selected
        post_instance = Owner.objects.create(username = UserName, password = Password, team = None)
        return post_instance.pk
    
    def CompleteOwner(OwnerID, league, team, TicsPer): #After team and tickets selected
        L = League.objects.get(name=league)
        T = Team.objects.get(name=team, league_id = L.id)
        return Owner.objects.filter(id=OwnerID).update(tickets=TicsPer, team_id=T.id)
    
    def GetLeagues():
        return League.objects.all()
    
    def GetLeague(LeagueName):
        return League.objects.filter(name=LeagueName)
    
    def GetLeagueName(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        T = Team.objects.get(id=O.team_id)
        L = League.objects.get(id=T.league_id)
        return L.name

    def GetTeams(league):
        return Team.objects.filter(league=league)
    
    def GetTeam(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        T = Team.objects.get(id=O.team_id)
        return T.name
    
    def GetTicsPer(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        return O.tickets 
        
    def GetTotalTics(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        T = O.team_id
        return Schedule.objects.filter(hometeam=T).count() * O.tickets
    
    def GetTeamID(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        T = O.team
        if T:
            return T.id
        return 0 # Team not selected yet
    
    def GetTicketsAssigned(OwnerID):
        TicketsAssigned = 0
        P = Person.objects.filter(owner_id=OwnerID)
        for p in P:
            T = Ticket.objects.filter(person = p)
            for t in T:
                TicketsAssigned += t.ticketsper * t.numbergames
        return TicketsAssigned

    def GetPersonCount(OwnerID):
        return Person.objects.filter(owner_id=OwnerID).count()
    
    def GetGameCount(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        T = Team.objects.get(id = O.team_id)
        return Schedule.objects.filter(hometeam = T.id).count()
    
    def GetPeopleTics(OwnerID):
        '''
Rendered in personinfo.html, people is 2D array, for rows of html table
        '''
        people = []
        TicsPer = DataJobs.GetTicsPer(OwnerID)
        P = Person.objects.filter(owner_id=OwnerID)
        for p in P:
            person = [] # Array of person name, number of 1 ticket games, 
            person.append(p.name)           # number of 2 ticket games etc.
            T = Ticket.objects.filter(person_id=p.id)
            for tp in range(TicsPer):
                s = None # for the space if none in html... default_if_none:"&nbsp"
                for t in T:
                    if t.ticketsper == tp + 1:
                        s = str(t.numbergames)
                        break
                person.append(s)
            people.append(person)
        return people

    def GetPersonArray(OwnerID):
        '''
Used to generate combos, each Person has an array of TicsPer, having an array
of tics/tics left, dictionary. Keeps track of how many tickets are left as 
combos are made. ticketsper is reverse order because combos
start with highest tickets
        '''
        Person = []
        P = DataJobs.GetPeople(OwnerID)
        for p in P:
            TicsPer = []
            T = Ticket.objects.filter(person_id=p.id).order_by('-ticketsper')
            for t in T:
                Tics = t.ticketsper
                Left = t.numbergames
                Dict = {
                    "StartTics": Tics,
                    "StartLeft": Left,
                    "Tics": Tics,
                    "Left": Left
                }
                TicsPer.append(Dict)
            Person.append(TicsPer)
        return Person
        
    def GetPeople(OwnerID):
        return Person.objects.filter(owner_id=OwnerID)
    
    def GetGames(OwnerID):
        O = Owner.objects.get(id=OwnerID)
        T = Team.objects.get(id = O.team_id)
        return Schedule.objects.filter(hometeam = T.id).order_by('date')
    
    def GetSchedule(OwnerID):
        '''
Rendered in requirements.html, and distribution.html, schedule is 2D array, 
for the 2 header rows of requirements and results tables.
        '''
        schedule = []
        S = DataJobs.GetGames(OwnerID)
        for s in S:
            DateCode = [] # Array of date, team code
            DateCode.append((s.date).strftime("%m/%d"))
            a = s.awayteam
            DateCode.append(a.code) 
            schedule.append(DateCode)
        return schedule
        
    def AddRequirement(Person, Game, Requirement):
        Req.objects.create(person = Person, game = Game, req = Requirement)
    
    def GetReqSched(OwnerID):
        '''
Rendered when returning to requirements.html after requirements assigned. Reqs is
2D array of requirements, each with person number, game number, requirement. Used
to populate table, each cell named as row/column like R1C4 (1st person, 4th game)
        '''
        Reqs = []
        games = DataJobs.GetGames(OwnerID)
        people = DataJobs.GetPeople(OwnerID)
        for PCount, p in enumerate(people):
            for GCount, g in enumerate(games):
                R = Req.objects.filter(person = p, game = g)
                for r in R: # Here we only add requirements to the array,
                    RC = []         # not entries for each person and game,
                    RC.append(PCount + 1)   # only person/games that have 
                    RC.append(GCount + 1)   # requirements. 
                    RC.append(r.req)
                    Reqs.append(RC)
        return Reqs
    
    def AddPerson(OwnerID, personName):
        O = Owner.objects.get(id=OwnerID)
        post_instance = Person.objects.create(owner = O, name = personName)
        return post_instance.pk
    
    def AddTicket(PersonID, TicsPer, NumberGames):
        P = Person.objects.get(id=PersonID)
        Ticket.objects.create(person = P, ticketsper = TicsPer, numbergames = NumberGames)
    
    def DeletePeopleTics(OwnerID):
        Person.objects.filter(owner_id=OwnerID).delete() #cascade delete for ticket
        
    def DeleteReqs(OwnerID):
        P = Person.objects.filter(owner_id=OwnerID)
        for p in P:
            Req.objects.filter(person_id=p.id).delete()
        
    def OnDistribution(OwnerID):
        ''' 
On distribution means get directed to distribution page. Check for results, then
check for requirements which would mean requirements assigned but Run was not hit
        '''
        Tries = DataJobs.GetTries(OwnerID)
        if Tries > 0:
            return True # there are results
        people = DataJobs.GetPeople(OwnerID)
        for p in people:
            if Req.objects.filter(person = p).count() > 0:
                return True # there are requirements
        return False
    
    def OnRequirements(OwnerID):
        ''' 
On requirements means get directed to requirements page. Check if all tickets
were assigned total tickets - tickets assigned (OnDistribution already false)
        '''
        t = DataJobs.GetTotalTics(OwnerID)
        if t == 0:
            return False # Team and tickets per game not yet selected
        if t - DataJobs.GetTicketsAssigned(OwnerID) == 0:
            return True
        return False
    
    def OnPerson(OwnerID):
        '''
On person means get directed to person info page. Check if team was assigned
(OnDistribution and OnRequirements already false)
        '''
        if DataJobs.GetTeamID(OwnerID) > 0:
            return True
        return False
    
    def AddBestTen(OwnerID, Diff, Bads, TenBestNbr):
        O = Owner.objects.get(id=OwnerID)
        BestTen.objects.create(owner = O, difference = Diff, bads = Bads, TenBestNumber = TenBestNbr)
        
    def DeleteBestTen(OwnerID):
        BestTen.objects.filter(owner_id = OwnerID).delete()
        
    def AddTenBest(PersonID, GameID, NumbTics, TenBestNbr):
        P = Person.objects.get(id = PersonID)
        G = Schedule.objects.get(id = GameID)
        TenBest.objects.create(person = P, game = G, NumberTickets = NumbTics, TenBestNumber = TenBestNbr)
        
    def DeleteTenBest(OwnerID):
        P = Person.objects.filter(owner_id = OwnerID)
        TenBest.objects.filter(person_id__in = P).delete()

    def AddStatus(PersonID, DupTeams, Bac2Bac, AvgRating, TenBestNbr):
        P = Person.objects.get(id = PersonID)
        Status.objects.create(person = P, DuplicateTeams = DupTeams, BackToBack = Bac2Bac, AverageRating = AvgRating, TenBestNumber = TenBestNbr)
        
    def DeleteStatus(OwnerID):
        P = Person.objects.filter(owner_id = OwnerID)
        Status.objects.filter(person_id__in = P).delete()
        
    def GetBestTenCount(OwnerID):
        return BestTen.objects.filter(owner_id = OwnerID).count()
    
    def Update10thBestTen(OwnerID, Diff, Bads):
        BestTen.objects.filter(owner_id = OwnerID, TenBestNumber = 10).update(difference = Diff, bads = Bads)
        
    def BumpBestTen(OwnerID, Diff, Bads, TenBestNbr, TlBestTen):
        if TlBestTen > 0:
            for t in range(TlBestTen, TenBestNbr - 1, -1):
                if t < 10:
                    BestTen.objects.filter(owner_id = OwnerID, TenBestNumber = t).update(TenBestNumber = t + 1)
                else:
                    BestTen.objects.filter(owner_id = OwnerID, TenBestNumber = t).delete()
        DataJobs.AddBestTen(OwnerID, Diff, Bads, TenBestNbr)
        
    def Update10thStatus(PersonID, Dups, BackToBacks, AverageRating):
        Status.objects.filter(person_id = PersonID, TenBestNumber = 10).update(DuplicateTeams = Dups, BackToBack = BackToBacks, AverageRating = AverageRating)
        
    def BumpStatus(PersonID, Dups, BackToBacks, AverageRating, TenBestNbr, TlBestTen):
        for t in range(TlBestTen, TenBestNbr - 1, -1):
            if t < 10:
                Status.objects.filter(person_id = PersonID, TenBestNumber = t).update(TenBestNumber = t + 1)
            else:
                Status.objects.filter(person_id = PersonID, TenBestNumber = t).delete()
        DataJobs.AddStatus(PersonID, Dups, BackToBacks, AverageRating, TenBestNbr)
        
    def BumpTenBest(OwnerID, TenBestNbr, TlBestTen):
        P = Person.objects.filter(owner_id = OwnerID)
        if TlBestTen == 10:
            TenBest.objects.filter(person_id__in = P, TenBestNumber = 10).delete()
        for t in range(TlBestTen, TenBestNbr - 1, -1):
            if t < 10:
                TenBest.objects.filter(person_id__in = P, TenBestNumber = t).update(TenBestNumber = t + 1)
            
    def AddTries(OwnerID, Tries):
        Owner.objects.filter(id = OwnerID).update(tries = Tries)
    
    def GetTries(OwnerID):
        O = Owner.objects.get(id = OwnerID)
        return O.tries
        
    def GetBestTen(OwnerID):
        '''
Rendered in distribution.html for the stats table, bestten is a 2D array
of bads, difference rows
        '''
        bestten = []
        B = BestTen.objects.filter(owner_id = OwnerID).order_by('TenBestNumber')
        for b in B:
            BTRow = []
            BTRow.append(str(b.difference)) # Had to make string because difference
            BTRow.append(b.bads)            # is a decimal value and wasn't 
            bestten.append(BTRow)           # recognized as numbers in html
        return (str(bestten)).replace("'", "") # and had to remove the string quotes
    
    def GetBest(OwnerID):
        return BestTen.objects.filter(owner_id = OwnerID).order_by('TenBestNumber')
    
    def GetGameIDs(OwnerID):
        IDs = []
        S = DataJobs.GetGames(OwnerID)
        for s in S:
            IDs.append(s.id)
        return IDs
    
    def GetPersonIDs(OwnerID):
        P = Person.objects.filter(owner_id = OwnerID)
        IDs = []
        for p in P:
            IDs.append(p.id)
        return IDs

    def GetTenBest(OwnerID, TenBestNbr):
        '''
Rendered in distribution.html, tenbest is a 2D array to populate the results
table. It's one of the ten best (TenBestNbr), all 10 are sent to 
distribution.html, plus minus buttons show each one.
        '''
        GameIDs = DataJobs.GetGameIDs(OwnerID) # Cells of the table are named as
        PersonIDs = DataJobs.GetPersonIDs(OwnerID) # row/column, like R2C1. What
        tenbest = []                        # this does is provide person number,
        P = Person.objects.filter(owner_id = OwnerID) # game number (row, col),
        T = TenBest.objects.filter(TenBestNumber=TenBestNbr, person_id__in=P)
        for t in T:                   # and number of tickets for each result.
            RowCol = []
            p = DataJobs.GetPersonNbrFromID(t.person_id, PersonIDs)
            g = DataJobs.GetGameNbrFromID(t.game_id, GameIDs)
            RowCol.append(p)
            RowCol.append(g)
            RowCol.append(t.NumberTickets)  
            tenbest.append(RowCol)
        return tenbest
        
    def GetPersonNbrFromID(ID, IDs):
        PersonNbr = 0
        for id in IDs:
            PersonNbr += 1
            if id == ID:
                return PersonNbr
                    
    def GetGameNbrFromID(ID, IDs):
        GameNbr = 0
        for id in IDs:
            GameNbr += 1
            if id == ID:
                return GameNbr
    
    def DistributionContext(OwnerID, TenBestNbr):
        '''
This is the context sent to distribution.html, put here because it's 
repeated several times for all the back buttons that send you there.
        '''
        newOwner = get_object_or_404(Owner, pk=OwnerID)
        schedule = DataJobs.GetSchedule(OwnerID) # 2 header rows for results table
        people = DataJobs.GetPeople(OwnerID)
        Tries = DataJobs.GetTries(OwnerID)
        BestTen = DataJobs.GetBestTen(OwnerID) # For the stats table
        PersonCnt = DataJobs.GetPersonCount(OwnerID)
        GameCnt = DataJobs.GetGameCount(OwnerID)
        TenBest1 = DataJobs.GetTenBest(OwnerID, 1) # best results
        TenBest2 = DataJobs.GetTenBest(OwnerID, 2) # 2nd best results
        TenBest3 = DataJobs.GetTenBest(OwnerID, 3)
        TenBest4 = DataJobs.GetTenBest(OwnerID, 4)
        TenBest5 = DataJobs.GetTenBest(OwnerID, 5)
        TenBest6 = DataJobs.GetTenBest(OwnerID, 6)
        TenBest7 = DataJobs.GetTenBest(OwnerID, 7)
        TenBest8 = DataJobs.GetTenBest(OwnerID, 8)
        TenBest9 = DataJobs.GetTenBest(OwnerID, 9)
        TenBest10 = DataJobs.GetTenBest(OwnerID, 10)
        return {'owner': newOwner, 'schedule': schedule, 'people': people, 'tries': Tries, 'bestten': BestTen, 'personcnt': PersonCnt, 'gamecnt': GameCnt, 'tenbest1': TenBest1, 'tenbest2': TenBest2, 'tenbest3': TenBest3, 'tenbest4': TenBest4, 'tenbest5': TenBest5, 'tenbest6': TenBest6, 'tenbest7': TenBest7, 'tenbest8': TenBest8, 'tenbest9': TenBest9, 'tenbest10': TenBest10, 'tenbestnbr': TenBestNbr}

    def GetPeopleStatus(OwnerID, TenBestNbr):
        return Status.objects.select_related().filter(person__owner__id = OwnerID, TenBestNumber = TenBestNbr)

    def GetReportInfo(OwnerID, TenBestNbr):
        return TenBest.objects.select_related().filter(person__owner__id = OwnerID, TenBestNumber = TenBestNbr).order_by('person', 'game__date')
    
    def NoResultEntry(OwnerID, CauseInfo):
        NoResult.objects.create(owner_id = OwnerID, causeinfo = CauseInfo)
    
    def GetNoResultMessages(OwnerID):
        return NoResult.objects.filter(owner_id = OwnerID)

    def CheckPersonMsg(PersonID):
        P = Person.objects.get(id=PersonID)
        return 'Check person ' + P.name
        
    def CheckGameMsg(GameID):
        S = Schedule.objects.get(id = GameID)
        return 'Check game ' + str(S.date)
        
    def DeleteNoResultMessages(OwnerID):
        NoResult.objects.filter(owner_id=OwnerID).delete()
    
    def GetGameArray(OwnerID):
        Game = []
        games = DataJobs.GetGames(OwnerID)
        GameIDs = DataJobs.GetGameIDs(OwnerID)
        for gCount, g in enumerate(games):
            P = DataJobs.GetPeople(OwnerID)
            Person = []
            for p in P:
                Person.append(DataJobs.GetReq(p.id, g.id))
            BackToBacks = []
            if gCount > 0:
                if DataJobs.AreBackToBack(OwnerID, g.date, games[gCount - 1].date):
                    BackToBacks.append(games[gCount - 1].id)
            if gCount < DataJobs.GetGameCount(OwnerID) - 1:
                if DataJobs.AreBackToBack(OwnerID, g.date, games[gCount + 1].date):
                    BackToBacks.append(games[gCount + 1].id)
            Dict = {
                "GameID": g.id,
                "GameNbrOrig": gCount, #before the shuffle
                "GameNbr": gCount,
                "TeamID": g.awayteam_id,
                "GameDate": g.date,
                "Rating": DataJobs.GetTeamRating(g.awayteam_id),
                "ReqGame": DataJobs.IsReqGame(OwnerID, g.id),
                "Person": Person,
                "BackToBacks": BackToBacks
            }
            Game.append(Dict)
        return Game
    
    def GetPersonTlTics(PersonID):
        TlTics = 0
        T = Ticket.objects.filter(person_id = PersonID)
        for t in T:
            TlTics += t.ticketsper * t.numbergames
        return TlTics
    
    def GetPersonGame(OwnerID):#, Combos):
        '''
        PersonGame = []
        G = DataJobs.GetGames(OwnerID)
        GameIDs = DataJobs.GetGameIDs(OwnerID)
        P = DataJobs.GetPeople(OwnerID)
        for pCount, p in enumerate(P):
            Person = []
            Person.append(p.id)
            Game = []
            for gCount, g in enumerate(G):
                Combo = Combos[gCount][pCount]
                if Combo > 0:
                    Dict = {
                        "Tics": Combo,
                        "GameID": GameIDs[gCount],
                        "TeamID": g.awayteam_id,
                        "GameDate": g.date,
                        "TeamRating": DataJobs.GetTeamRating(g.awayteam_id)
                    }
                    Game.append(Dict)
            Person.append(Game)
            PersonGame.append(Person)
        return PersonGame
        '''
        PersonGame = []
        G = DataJobs.GetGames(OwnerID)
        GameIDs = DataJobs.GetGameIDs(OwnerID)
        P = DataJobs.GetPeople(OwnerID)
        for pCount, p in enumerate(P):
            Person = []
            Person.append(p.id)
            TlTicketGames = DataJobs.GetTicketGames(p.id)
            Game = []
            for t in range(TlTicketGames):
                Dict = {
                    "Tics": 0,
                    "GameID": 0,
                    "TeamID": 0,
                    "GameDate": 0,
                    "TeamRating": 0
                } 
                Game.append(Dict)               
            Person.append(Game)
            PersonGame.append(Person)
        return PersonGame

    def GetTicketGames(PersonID):
        TicketGames = 0
        N = Ticket.objects.filter(person_id = PersonID)
        for n in N:
            TicketGames += n.numbergames
        return TicketGames
            
    def GetTeamRating(TeamID): 
        T = Team.objects.get(id=TeamID)  
        return T.rating   
    
            
    def AreBackToBack(OwnerID, CurrDate, PrevDate):
        TeamID = DataJobs.GetTeamID(OwnerID)
        B = Schedule.objects.filter(Q(awayteam_id = TeamID) | Q(hometeam = TeamID), date__gt = PrevDate, date__lt = CurrDate)
       # print('CurrDate')
     #   print(str(CurrDate))
      #  print('PrevDate')
     #   print(str(PrevDate))
     #   print('B.count() is ' + str(B.count()))
        if B.count() == 0:
            return True
        return False 
    
    def IsReqGame(OwnerID, GameID):
        P = Person.objects.filter(owner_id=OwnerID)
        if Req.objects.filter(game_id = GameID, person_id__in = P).count() > 0:
            return True
        return False
            
    def GetReq(PersonID, GameID):
        R = Req.objects.filter(game_id = GameID, person_id = PersonID)
        if R.count() == 0:
            return None
        for r in R: # there's only one but had to use filter
            return r.req
        
    def GetReqGames(OwnerID, Games):
        ReqGames = []
        for g in Games:
            if DataJobs.IsReqGame(OwnerID, g['GameID']):
                ReqGames.append(g)
        return ReqGames
    
    def NoGetReqGames(OwnerID, Games):
        NoReqGames = []
        for g in Games:
            if DataJobs.IsReqGame(OwnerID, g['GameID']):
                ReqGames.append(g)
        return ReqGames
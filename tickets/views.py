from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Owner, League #do we need these?
from .ScheduleImport import ImportSchedule
from .TicketsInfo import DataJobs
from .Distribution import Distribute
from decimal import Decimal

def index(request):
    if request.method == "POST":
        FromDist = False
        userName = request.POST['Name']
        password = request.POST['Pwd']
        owner = DataJobs.GetOwner(userName, password)
        if 'btnNewUser' in request.POST:
            #New user so don't expect existing userName/password, if found return to Index page
            if owner:
                return render(request, 'tickets/index.html')
            ownerID = DataJobs.AddInitialOwner(userName, password) # Owner will be updated later
            newOwner = get_object_or_404(Owner, pk=ownerID)
            leagues = DataJobs.GetLeagues()
            TicsPer = None
            context = {'owner': newOwner, 'leagues': leagues, 'ticsper': TicsPer, 'fromdist': FromDist}
            return render(request, 'tickets/ticketInfo.html', context)
        if 'btnExistingUser' in request.POST:
            #Existing user so expect existing userName/password, if not found return to Index page
            if owner:#There's only one owner but filter was used because there might not have
                for o in owner:#been an owner, that's why we're looping
                    ownerID = o.id
                newOwner = get_object_or_404(Owner, pk=ownerID) 
                NoResultMessages = DataJobs.GetNoResultMessages(ownerID)
                # NoResultMessages should only come from person info or requirements
                # so only check there below
                if DataJobs.OnDistribution(ownerID): # Successful results or requirements assigned
                    context = DataJobs.DistributionContext(ownerID, 1)
                    return render(request, 'tickets/distribution.html', context)
                if DataJobs.OnRequirements(ownerID):
                    if NoResultMessages.count() > 0:
                        From = 'People'
                        context = {'owner': newOwner, 'noresultmessages': NoResultMessages, 'from': From}
                        return render(request, 'tickets/noresult.html', context)
                    TicsPer = DataJobs.GetTicsPer(ownerID)
                    schedule = DataJobs.GetSchedule(ownerID)
                    people = DataJobs.GetPeople(ownerID)
                    context = {'owner': newOwner, 'ticsperrange': range(1, TicsPer+1), 'schedule': schedule, 'people': people, 'fromdist': FromDist}
                    return render(request, 'tickets/requirements.html', context)
                if DataJobs.OnPerson(ownerID):
                    TicsRemaining = DataJobs.GetTotalTics(ownerID) - DataJobs.GetTicketsAssigned(ownerID)
                    TicsPer = DataJobs.GetTicsPer(ownerID)
                    PersonCount = DataJobs.GetPersonCount(ownerID)
                    #newOwner = get_object_or_404(Owner, pk=ownerID)
                    peopleTics = DataJobs.GetPeopleTics(ownerID)
                    context = {'owner': newOwner, 'ticsperrange': range(TicsPer), 'ticsperrange2': range(2, int(TicsPer)+2), 'ticsremaining': TicsRemaining, 'personcount': range(PersonCount), 'people': peopleTics, 'nextperson': PersonCount+1, 'fromdist': FromDist}
                    return render(request, 'tickets/personInfo.html', context)
                # On tickets
                #newOwner = get_object_or_404(Owner, pk=ownerID)
                leagues = DataJobs.GetLeagues()
                TicsPer = None
                context = {'owner': newOwner, 'leagues': leagues, 'ticsper': TicsPer, 'fromdist': FromDist}
                return render(request, 'tickets/ticketInfo.html', context)
            return render(request, 'tickets/index.html')
        if 'btnNHLTeams' in request.POST:
            ImportSchedule.ImportNHLTeams()  #CAREFUL DON"T RUN LOCAL!
            context = {'admin': True }
            return render(request, 'tickets/index.html', context) 
        if 'btnNBATeams' in request.POST:
            ImportSchedule.ImportNBATeams()  #CAREFUL DON"T RUN LOCAL!
            context = {'admin': True }
            return render(request, 'tickets/index.html', context) 
        if 'btnNFLTeams' in request.POST:
            ImportSchedule.ImportNFLTeams()  #CAREFUL DON"T RUN LOCAL!
            context = {'admin': True }
            return render(request, 'tickets/index.html', context) 
        if 'btnNHLSchedule' in request.POST:
            ImportSchedule.ImportNHLSchedule()  #CAREFUL DON"T RUN LOCAL!
            context = {'admin': True }
            return render(request, 'tickets/index.html', context) 
        if 'btnNBASchedule' in request.POST:
            ImportSchedule.ImportNBASchedule()  #CAREFUL DON"T RUN LOCAL!
            context = {'admin': True }
            return render(request, 'tickets/index.html', context) 
        if 'btnNFLSchedule' in request.POST:
            ImportSchedule.ImportNFLSchedule()  #CAREFUL DON"T RUN LOCAL!
            context = {'admin': True }
            return render(request, 'tickets/index.html', context) 
    else:
       # ImportSchedule.ImportNHLTeams() #administrative tool
      #  Distribute.Test()
        leagues = DataJobs.GetLeagues()
        return render(request, 'tickets/index.html', {'leagues': leagues}) 
    
def ticketinfo(request, owner_id):
    if request.method == "POST":
        league = request.POST['HomeLeague']
        L = DataJobs.GetLeague(league)
        newOwner = get_object_or_404(Owner, pk=owner_id)
        #had to use for loop even though only 1 record
        for l in L:
            teams = DataJobs.GetTeams(l)
        if 'btnSubmitLeague' in request.POST:
            leagues = DataJobs.GetLeagues()
            TicsPer = None
            FromDist = False
            context = {'owner': newOwner, 'teams': teams, 'leagues': leagues, 'league': league, 'ticsper': TicsPer, 'fromdist': FromDist}
            return render(request, 'tickets/ticketInfo.html', context)
        if 'btnBack' in request.POST:
            context = DataJobs.DistributionContext(owner_id, 1)
            return render(request, 'tickets/distribution.html', context) 
        #btnSubmitAll was clicked
        team = request.POST['HomeTeam']
        TicsPer = request.POST['TicsPer']
        DataJobs.CompleteOwner(owner_id, league, team, TicsPer)
        TotalTics = DataJobs.GetTotalTics(owner_id)
        peopleTics = DataJobs.GetPeopleTics(owner_id)
        FromDist = False
        context = {'owner': newOwner, 'ticsperrange': range(int(TicsPer)), 'ticsperrange2': range(2, int(TicsPer)+2), 'ticsremaining': TotalTics, 'personcount': range(0), 'people': peopleTics, 'nextperson': 1, 'fromdist': FromDist}
        return render(request, 'tickets/personInfo.html', context)
    else:
        return render(request, 'tickets/ticketInfo.html')
    
def personinfo(request, owner_id):
    if request.method == "POST":
        newOwner = get_object_or_404(Owner, pk=owner_id)
        if 'btnBack' in request.POST:
            context = DataJobs.DistributionContext(owner_id, 1)
            return render(request, 'tickets/distribution.html', context) 
        PersonCount = DataJobs.GetPersonCount(owner_id) # before adding people
        DataJobs.DeletePeopleTics(owner_id)
        TicsPer = DataJobs.GetTicsPer(owner_id) # before adding people
        FD = request.POST['FromDist']
        if FD == 'FDYes':
            ExtraPerson = 0
        elif FD == 'FDNo':
            ExtraPerson = 1
        for p in range(PersonCount + ExtraPerson):
            PersonName = request.POST['T'+str(p+1)+',1']
            if PersonName != '':
                personID = DataJobs.AddPerson(owner_id, PersonName)
                for t in range(2, TicsPer+2):
                    NumberOfGames = request.POST['T'+str(p+1)+','+str(t)]
                    if (NumberOfGames.strip()).isnumeric():    
                        DataJobs.AddTicket(personID, t-1, NumberOfGames)
        if DataJobs.GetTotalTics(owner_id) - DataJobs.GetTicketsAssigned(owner_id) == 0:
            success = Distribute.DoCombos('People')
            if success == True:
                schedule = DataJobs.GetSchedule(owner_id)
                people = DataJobs.GetPeople(owner_id)
                FromDist = False
                context = {'owner': newOwner, 'ticsperrange': range(1, TicsPer+1), 'schedule': schedule, 'people': people, 'fromdist': FromDist}            
                return render(request, 'tickets/requirements.html', context)
            else:
                NoResultMessages = DataJobs.GetNoResultMessages(owner_id)
                if NoResultMessages.count() > 0:
                    From = 'People'
                    context = {'owner': newOwner, 'noresultmessages': NoResultMessages, 'from': From}
                    return render(request, 'tickets/noresult.html', context)
        TicsRemaining = DataJobs.GetTotalTics(owner_id) - DataJobs.GetTicketsAssigned(owner_id)
        TicsPer = DataJobs.GetTicsPer(owner_id) # after adding people
        PersonCount = DataJobs.GetPersonCount(owner_id) # after adding people
        peopleTics = DataJobs.GetPeopleTics(owner_id)
        FromDist = False
        context = {'owner': newOwner, 'ticsperrange': range(TicsPer), 'ticsperrange2': range(2, int(TicsPer)+2), 'ticsremaining': TicsRemaining, 'personcount': range(PersonCount), 'people': peopleTics, 'nextperson': PersonCount+1, 'fromdist': FromDist}
        return render(request, 'tickets/personInfo.html', context)
    else:
        print('hey')
        newOwner = get_object_or_404(Owner, pk=owner_id)
        context = {'owner': newOwenr}
        return render(request, 'tickets/personInfo.html', context)
    
def requirements(request, owner_id):
    newOwner = get_object_or_404(Owner, pk=owner_id)
    schedule = DataJobs.GetSchedule(owner_id)
    people = DataJobs.GetPeople(owner_id)
    if request.method == "POST":
        if 'btnBack' in request.POST:
            context = DataJobs.DistributionContext(owner_id, 1)
            return render(request, 'tickets/distribution.html', context)
        DataJobs.DeleteReqs(owner_id)
        games = DataJobs.GetGames(owner_id)
        PersonCount = 0
        for p in people:
            PersonCount += 1
            GameCount = 0
            for g in games:
                GameCount += 1
                s = request.POST['R'+str(PersonCount)+'C'+str(GameCount)]
                if s == 'no':
                    DataJobs.AddRequirement(p, g, 0)
                elif s.isnumeric():
                    DataJobs.AddRequirement(p, g, int(s))
        context = {'owner': newOwner, 'schedule': schedule, 'people': people, 'tries': 0}
        return render(request, 'tickets/distribution.html', context)
    else:
        context = {'owner': newOwner, 'schedule': schedule, 'people': people}
        return render(request, 'tickets/personInfo.html', context)
    
def distribution(request, owner_id):
    FromDist = True
    newOwner = get_object_or_404(Owner, pk=owner_id)
    TicsPer = DataJobs.GetTicsPer(owner_id)
    peopleTics = DataJobs.GetPeopleTics(owner_id)
    schedule = DataJobs.GetSchedule(owner_id)
    if request.method == "POST":
        if 'btnTickets' in request.POST:
            leagues = DataJobs.GetLeagues()
            league = DataJobs.GetLeagueName(owner_id)
            print('League is ' + league)
            L = DataJobs.GetLeague(league)
            for l in L:
                teams = DataJobs.GetTeams(l)
            team = DataJobs.GetTeam(owner_id)
            context = {'owner': newOwner, 'leagues': leagues, 'league': league, 'teams': teams, 'team': team, 'ticsper': TicsPer, 'fromdist': FromDist}
            return render(request, 'tickets/ticketInfo.html', context)
        if 'btnPeople' in request.POST: 
            TicsRemaining = DataJobs.GetTotalTics(owner_id) - DataJobs.GetTicketsAssigned(owner_id)
            context = {'owner': newOwner, 'ticsperrange': range(TicsPer), 'ticsperrange2': range(2, TicsPer+2), 'ticsremaining': TicsRemaining, 'personcount': range(0), 'people': peopleTics, 'nextperson': 1, 'fromdist': FromDist}
            return render(request, 'tickets/personInfo.html', context) 
        if 'btnRequirements' in request.POST: 
            ReqString = DataJobs.GetReqSched(owner_id)
            people = DataJobs.GetPeople(owner_id)
            context = {'owner': newOwner, 'ticsperrange': range(1, TicsPer+1), 'schedule': schedule, 'people': people, 'fromdist': FromDist, 'reqstring': ReqString}
            return render(request, 'tickets/requirements.html', context)
        if 'btnRun' in request.POST:
            m = request.POST['Minutes']
            if Distribute.Run(owner_id, int(m)):
                context = DataJobs.DistributionContext(owner_id, 1)
                return render(request, 'tickets/distribution.html', context)
            NoResultMessages = DataJobs.GetNoResultMessages(owner_id)
            From = 'Run'
            context = {'owner': newOwner, 'noresultmessages': NoResultMessages, 'from': From}
            return render(request, 'tickets/noresult.html', context)
        if 'btnDetails' in request.POST:
            TB = int(request.POST['TenBestNumber'])
            PeopleStatus = DataJobs.GetPeopleStatus(owner_id, TB)
            context = {'owner': newOwner, 'peoplestatus': PeopleStatus, 'tenbestnbr': TB}
            return render(request, 'tickets/details.html', context)
        if 'btnReport' in request.POST:
            TB = int(request.POST['TenBestNumber'])
            ReportInfo = DataJobs.GetReportInfo(owner_id, TB)
            context = {'owner': newOwner, 'reportinfo': ReportInfo, 'tenbestnbr': TB}
            return render(request, 'tickets/report.html', context)
        return render(request, 'tickets/distribution.html', context)
    else:
        return render(request, 'tickets/distribution.html', context)
    
def details(request, owner_id):
    if request.method == "POST":
        TenBestNbr = request.POST['TenBestNbr']
        context = DataJobs.DistributionContext(owner_id, TenBestNbr)
        return render(request, 'tickets/distribution.html', context)
    
def report(request, owner_id):
    if request.method == "POST":
        TenBestNbr = request.POST['TenBestNbr']
        context = DataJobs.DistributionContext(owner_id, TenBestNbr)
        return render(request, 'tickets/distribution.html', context)
    
def noresult(request, owner_id):
    if request.method == 'POST':
        newOwner = get_object_or_404(Owner, pk=owner_id)
        TicsPer = DataJobs.GetTicsPer(owner_id)
        FromDist = False
        From = request.POST['From']
        if From == 'People':
            peopleTics = DataJobs.GetPeopleTics(owner_id) # people in personInfo.html
            PersonCount = DataJobs.GetPersonCount(owner_id)
            TicsRemaining = DataJobs.GetTotalTics(owner_id) - DataJobs.GetTicketsAssigned(owner_id)
            context = {'owner': newOwner, 'ticsperrange': range(TicsPer), 'ticsperrange2': range(2, TicsPer+2), 'ticsremaining': TicsRemaining, 'personcount': range(PersonCount), 'people': peopleTics, 'nextperson': PersonCount+1, 'fromdist': FromDist}
            return render(request, 'tickets/personInfo.html', context) 
        if From == 'Run':
            ReqString = DataJobs.GetReqSched(owner_id)
            people = DataJobs.GetPeople(owner_id)
            schedule = DataJobs.GetSchedule(owner_id)
            context = {'owner': newOwner, 'ticsperrange': range(1, TicsPer+1), 'schedule': schedule, 'people': people, 'fromdist': FromDist, 'reqstring': ReqString}
            return render(request, 'tickets/requirements.html', context)
        context = DataJobs.DistributionContext(owner_id, 1)
        return render(request, 'tickets/distribution.html', context)
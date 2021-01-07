from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import League, Team, Schedule
from django.conf import settings
from datetime import datetime
from .TicketsInfo import DataJobs

class ImportSchedule:
    
    def ImportNHLTeams():
        file_path = settings.BASE_DIR
        L = League.objects.get(name='NHL')
        DataJobs.DeleteTeams('NHL')
        with open(file_path + '//NHLTeams.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            post_instance = Team.objects.create(league = L, name = words[1], rating = words[2], code = words[0])

    def ImportNBATeams():
        file_path = settings.BASE_DIR
        L = League.objects.get(name='NBA')
        DataJobs.DeleteTeams('NBA')
        with open(file_path + '//NBATeams.TXT', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            post_instance = Team.objects.create(league = L, name = words[1], rating = words[2], code = words[0])

    def ImportNFLTeams():
        file_path = settings.BASE_DIR
        L = League.objects.get(name='NFL')
        DataJobs.DeleteTeams('NFL')
        with open(file_path + '//NFLTeams.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            post_instance = Team.objects.create(league = L, name = words[1], rating = words[2], code = words[0])
                    
    def ImportNHLSchedule():
        file_path = settings.BASE_DIR
        DataJobs.DeleteSchedule('NHL')
        with open(file_path + '//NHLSchedule.TXT', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            id = DataJobs.GetLeagueID('NHL')
            H = Team.objects.get(name=words[1], league_id=id)
            HomeID = H.id
            A = Team.objects.get(name=words[2].rstrip('\n'), league_id=id)
            date_object = datetime.strptime(words[0], "%m/%d/%y")
            post_instance = Schedule.objects.create(date = date_object, hometeam = HomeID, awayteam = A)   
            
    def ImportNBASchedule():
        file_path = settings.BASE_DIR
        DataJobs.DeleteSchedule('NBA')
        with open(file_path + '//NBASchedule.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            id = DataJobs.GetLeagueID('NBA')
            H = Team.objects.get(name=words[1], league_id=id)
            HomeID = H.id
            A = Team.objects.get(name=words[2].rstrip('\n'), league_id=id)
            date_object = datetime.strptime(words[0], "%m/%d/%y")
            post_instance = Schedule.objects.create(date = date_object, hometeam = HomeID, awayteam = A) 
            
    def ImportNFLSchedule():
        file_path = settings.BASE_DIR
        DataJobs.DeleteSchedule('NFL')
        with open(file_path + '//NFLSchedule.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            id = DataJobs.GetLeagueID('NFL')
            H = Team.objects.get(name=words[1], league_id=id)
            HomeID = H.id
            A = Team.objects.get(name=words[2].rstrip('\n'), league_id=id)
            date_object = datetime.strptime(words[0], "%m/%d/%y")
            post_instance = Schedule.objects.create(date = date_object, hometeam = HomeID, awayteam = A) 

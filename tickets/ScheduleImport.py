from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import League, Team, Schedule
from django.conf import settings
from datetime import datetime
from .TicketsInfo import DataJobs

class ImportSchedule:
        
    def ImportTeams(league):
        file_path = settings.BASE_DIR
        L = League.objects.get(name=league)
        #DataJobs.DeleteTeams(league)
        with open(file_path + '//' + league + 'Teams.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            team = Team.objects.filter(league=L, name=words[1], code=words[0])
            if team:
                post_instance = Team.objects.filter(league=L, name=words[1], code=words[0]).update(rating=words[2])
            else:
                post_instance = Team.objects.create(league = L, name = words[1], rating = words[2], code = words[0]) 
    
    def ImportSchedule(league):
        file_path = settings.BASE_DIR
        DataJobs.DeleteLastYear(league)
        DataJobs.FlagLastYear(league)
        with open(file_path + '//' + league + 'Schedule.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            id = DataJobs.GetLeagueID(league)
            H = Team.objects.get(name=words[1], league_id=id)
            HomeID = H.id
            A = Team.objects.get(name=words[2].rstrip('\n'), league_id=id)
            date_object = datetime.strptime(words[0], "%m/%d/%y")
            post_instance = Schedule.objects.create(date = date_object, hometeam = HomeID, awayteam = A)  
    

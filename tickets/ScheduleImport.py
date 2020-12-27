from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import League, Team, Schedule
from django.conf import settings
from datetime import datetime

class ImportSchedule:
    
    def ImportLeague():
        post_instance = League.objects.create(name = 'NBA')
        
    def ImportNHLTeams():
        file_path = settings.BASE_DIR
        L = League.objects.get(name='NHL')
        Team.objects.all().delete()
        with open(file_path + '\\Teams.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            post_instance = Team.objects.create(league = L, name = words[1], rating = words[3], code = words[0])
            
            #for word in words:
                
        #L = League.objects.get(name='NHL')
        #post_instance = Team.objects.create(league = L, name = 'Flyers', rating = 10, code = 'PHI')

    def ImportNBATeams():
        file_path = settings.BASE_DIR
        L = League.objects.get(name='NBA')
        #Team.objects.all().delete()
        with open(file_path + '\\Teams.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            post_instance = Team.objects.create(league = L, name = words[1], rating = words[2], code = words[0])
            
    def FormatTeams():
        file_path = settings.BASE_DIR
        with open(file_path + '\\TeamsCodes.txt', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        with open('Out.txt', 'w', encoding = 'utf-8') as f:
            tot = 0
            L = len(content)
            for line in content:
                tot += 1
                line = line.rstrip('\n')
                for c in line:
                    if ord(c) == 9:
                        f.write('|')
                    else:
                        f.write(c)
                if tot < L:
                    f.write('\n')
                    
    def ImportLeagueSchedule():
        file_path = settings.BASE_DIR
        Schedule.objects.all().delete()
        with open(file_path + '\\NHLP.TXT', 'r', encoding = 'utf-8') as f:
            content = f.readlines()
        for line in content:
            words = line.split('|')
            H = Team.objects.get(name=words[1], league_id=5)
            HomeID = H.id
            A = Team.objects.get(name=words[2].rstrip('\n'), league_id=5)
            date_object = datetime.strptime(words[0], "%m/%d/%y")
            post_instance = Schedule.objects.create(date = date_object, hometeam = HomeID, awayteam = A)   

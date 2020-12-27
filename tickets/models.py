from django.db import models

class League(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    rating = models.IntegerField()
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
class Owner(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    # Make team optional for creating owner before team selected
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    tickets = models.IntegerField(default=0)
    tries = models.IntegerField(default=0)
    
class Schedule(models.Model):
    hometeam = models.IntegerField() #.CharField(max_length=20)
    awayteam = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField()
    
class Person(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    
class Ticket(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    ticketsper = models.IntegerField()
    numbergames = models.IntegerField()
    
class Req(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    game = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    req = models.IntegerField()
    
class BestTen(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    difference = models.DecimalField(max_digits=7, decimal_places=5)
    bads = models.IntegerField()
    TenBestNumber = models.IntegerField()
    
class TenBest(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    game = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    NumberTickets = models.IntegerField()
    TenBestNumber = models.IntegerField()
    
class Status(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    DuplicateTeams = models.IntegerField()
    BackToBack = models.IntegerField()
    AverageRating = models.DecimalField(max_digits=7, decimal_places=5)
    TenBestNumber = models.IntegerField()
    
class NoResult(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    causeinfo = models.CharField(max_length=100)
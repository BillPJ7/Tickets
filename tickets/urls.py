from django.urls import path
from . import views
app_name = 'tickets'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:owner_id>/ticketinfo/', views.ticketinfo, name='ticketinfo'),
    path('<int:owner_id>/personinfo/', views.personinfo, name='personinfo'),
    path('<int:owner_id>/requirements/', views.requirements, name='requirements'),
    path('<int:owner_id>/distribution/', views.distribution, name='distribution'),
    path('<int:owner_id>/details/', views.details, name='details'),
    path('<int:owner_id>/report/', views.report, name='report'),
    path('<int:owner_id>/noresult/', views.noresult, name='noresult'),
]
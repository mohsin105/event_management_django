from django.shortcuts import render
from events.models import Event

# Create your views here.

def home(request): #prefetch_related name replaced from 'participant_list'
    return render(request,'home.html')

def no_permission(request):
    return render(request,'no_permission.html')

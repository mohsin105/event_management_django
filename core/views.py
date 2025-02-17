from django.shortcuts import render
from events.models import Event

# Create your views here.

def home(request): #prefetch_related name replaced from 'participant_list'
    events=Event.objects.select_related('category').prefetch_related('participants').all()
    context={'events':events}
    return render(request,'home.html',context)

def no_permission(request):
    return render(request,'no_permission.html')

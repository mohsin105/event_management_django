from django.shortcuts import render
from events.models import Event

# Create your views here.

def home(request): #prefetch_related name replaced from 'participant_list'
    events=Event.objects.select_related('category').prefetch_related('participants').all()
    if request.method=="POST":
        search_value = request.POST.get('search')
        search_type = request.POST.get('search_type')
        print(search_value)
        print('Search Type: ', search_type)
        if search_type=="category":
            print('inside category search')
            events=events.filter(category__name__icontains=search_value)
        else:
            events=events.filter(name__icontains=search_value)
            
    context={'events':events}
    return render(request,'home.html',context)

def no_permission(request):
    return render(request,'no_permission.html')

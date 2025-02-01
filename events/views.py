from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'home.html')
    

def event(request):
    return HttpResponse("This is the list of all events")

def event_form(request):
    return HttpResponse('this is the event form page to create, update an event')

def details(request):
    return HttpResponse('This is the details page of an event. ')
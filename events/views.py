from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm
from events.models import Event,Category
from django.contrib import messages
from datetime import date
from django.db.models import Q,Count
from django.contrib.auth.decorators import login_required,user_passes_test
from users.views import is_admin,is_organizer,admin_or_organizer

# Create your views here.

    

def event(request):
    return HttpResponse("This is the list of all events")

@user_passes_test(admin_or_organizer,login_url='no-permission')
def create_event(request):
    event_form=EventModelForm()

    if request.method=='POST':
        event_form=EventModelForm(request.POST,request.FILES)
        if event_form.is_valid():
            event=event_form.save(commit=False)
            event_form.save()
            # context={'event_form':event_form,'message':"Event Created Succesfully!"}
            # return render(request,'create_event.html',context)

            participants=request.POST.getlist('participants',[])
            print(participants)
            print(request.POST)
            if participants:
                event.participants.set(participants)
                

            messages.success(request,'Event created successfully!')
            context={'event_form':event_form}
            return redirect('create-event')
        else:
            # context={'event_form':event_form,'message':'Properly fill up the form!'}
            # return render(request,'create_event.html',context)
            messages.error(request,'Properly fill up the form!')
            return redirect('create-event')
        
    context={ 'event_form':event_form}
    return render(request,'create_event.html',context)

@user_passes_test(admin_or_organizer,login_url='no-permission')
def create_category(request):
    category_form=CategoryModelForm()

    if request.method=='POST':
        category_form=CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,'Category created successfully!')
            context={'category_form':category_form}
            return redirect('create-category')
        else:
            messages.error(request,'Properly fill up the form!')
            return redirect('create-category')
    
    context={'category_form':category_form}
    return render(request,'create_category.html',context)


@user_passes_test(admin_or_organizer,login_url='no-permission')
def update_event(request,id):
    event=Event.objects.get(id=id)
    event_form=EventModelForm(instance=event)

    if request.method=='POST':
        event_form=EventModelForm(request.POST,instance=event)
        if event_form.is_valid():
            event=event_form.save(commit=False)
            event_form.save()

            participants=request.POST.getlist('participants')
            # event.participant_list.set(participants)
            print('participant  list: ')
            print(participants)

            for member in participants:
                event.participants.add(member)  #prefetch_related name replaced from 'participant_list'

            messages.success(request,'Event Updated Succesfully!')
            return redirect('update-event',id)
        else:
            messages.error(request,'Something went wrong')
            return redirect('update-event',id)
            
    context={'event_form':event_form}
    return render(request,'create_event.html',context)


#organizer_dashboard
def show_dashboard(request):
    query_type=request.GET.get('type')
    events=Event.objects.select_related('category').prefetch_related('participants') #prefetch_related name replaced from 'participant_list'

    event_count=Event.objects.aggregate(total=Count('id',distinct=True),
                                        upcoming=Count('id',filter=Q(date__gt=date.today()),distinct=True),
                                        past=Count('id',filter=Q(date__lt=date.today()),distinct=True),
                                        unique_participants=Count('participants',distinct=True)
                                        ) #prefetch_related name replaced from 'participant_list'

    if query_type=='total':
        title='Total Events'
        events=events.all()
        
    elif query_type=='upcoming':
        title='Upcoming Events'
        events=events.filter(date__gt=date.today())
    elif query_type=='past':
        title='Past Events'
        events=events.filter(date__lt=date.today())
    else:
        upcomingEvents=Event.objects.filter(date__gt=date.today())
        # getting the most recent upcoming event
        # events=upcomingEvents.order_by('date')
        title='Todays Events'
        events=events.filter(date__exact=date.today())
        
    context={
             'events':events,
             'title':title,
             'event_count':event_count}
    return render(request,'dashboard.html',context)

def show_details(request,id): #prefetch_related name replaced from 'participant_list'
    event=Event.objects.prefetch_related('participants').get(id=id)

    context={'event':event}

    return render(request,'event_details.html',context)

@user_passes_test(admin_or_organizer,login_url='no-permission')
def delete_event(request,id):
    if request.method=='POST':
        event=Event.objects.get(id=id)
        event.delete()
        messages.success(request,'Event deleted!!')
        return redirect('dashboard')
    else:
        messages.error(request,'Event NOT deleted')
        return redirect('dashboard')

@user_passes_test(admin_or_organizer,login_url='no-permission')
def delete_category(request,id):
    if request.method=='POST':
        category=Category.objects.get(id=id)
        category.delete()
        messages.success(request,'Category deleted!!')
        return redirect('dashboard')
    else:
        messages.error(request,'Category NOT deleted')
        return redirect('dashboard')




    
    
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from users.forms import ParticipantModelForm,AssignRoleForm,CreateGroupForm
from events.models import Event
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()



def admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

#sign-up user
def create_participant(request):
    participant_form=ParticipantModelForm()

    if request.method=='POST':
        participant_form=ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            user=participant_form.save(commit=False)
            print(user)
            user.set_password(participant_form.cleaned_data.get('password1'))
            user.is_active=False
            print(participant_form.cleaned_data)
            user.save()
            # participant_form.save()
            messages.success(request,"A confirmation mail sent to your email. please check")
            return redirect('sign-in')
        else:
            messages.error(request,'Properly fill up the form!')
            return redirect('create-participant')

    context={'participant_form':participant_form}
    return render(request,'registration/create_participant.html',context)

# verifying the token
def activate_user(reqeust,user_id,token):
    user=User.objects.get(id=user_id)
    try:
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User Not found")


def sign_in(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
            
    return render(request,'registration/login.html',{'form':form})



@login_required
def sign_out(request):
    if request.method=='POST':
        logout(request)
        return redirect('sign-in')

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRoleForm()

    if request.method =='POST':
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)

            messages.success(request,f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')

    context={'form':form}
    return render(request,'admin/assign_role.html',context)

def show_participants(request):
    users=User.objects.prefetch_related('rsvp_events').all()

    context={'users':users}
    return render(request,'admin/user_list.html',context)


@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method=='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f'Group {group.name} created successfully')
            return redirect('create-group')
    
    context={'form':form}
    return render(request,'admin/create_group.html',context)

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups=Group.objects.prefetch_related('permissions').all()
    context={'groups':groups}
    return render(request,'admin/group_list.html',context)

@user_passes_test(is_admin,login_url='no-permission')
def delete_participant(request,id):
    if request.method=='POST':
        user=User.objects.get(id=id)
        user.delete()
        messages.success(request,'Participant removed!!')
        return redirect('dashboard')
    else:
        messages.error(request,'Participant NOT removed')
        return redirect('dashboard')

@user_passes_test(is_admin,login_url='no-permission')
def delete_group(request,id):
    if request.method=='POST':
        group=Group.objects.get(id=id)
        group.delete()
        messages.success(request,'Group removed!!')
        return redirect('dashboard')
    else:
        messages.error(request,'Group NOT removed')
        return redirect('dashboard')

@login_required
def rsvp_to_events(request,event_id):
    if request.method =='POST':
        user=request.user
        event=Event.objects.get(id=event_id)
        if user.rsvp_events.filter(id=event_id).exists():
            messages.error(request,"You have already registered this event")
            return redirect('user-dashboard')
        else:
            user.rsvp_events.add(event)
            messages.success(request,"Event successfully registered")
            return redirect('user-dashboard')


@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    # return render(request,'dashboard/dashboard.html')
    return redirect('no-permission')


def admin_dashboard(request):
    query_type=request.GET.get('type')
    if query_type=='participants':
        contents=User.objects.all()
    else:
        contents=Event.objects.all()
    context={'contents':contents}
    return render(request,'admin/admin_dashboard.html',context)

def user_dashboard(request):
    user=request.user
    context={'user':user}
    return render(request,'dashboard/user_dashboard.html')

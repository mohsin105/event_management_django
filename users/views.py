from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from users.forms import ParticipantModelForm,AssignRoleForm,CreateGroupForm,EditProfileForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, CustomLoginForm
from events.models import Event,Category
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView,TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView,PasswordResetConfirmView
from datetime import date
from django.db.models import Q,Count

User=get_user_model()

# Role Control Functions ------------> 
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()



def admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

def admin_or_owner(user, event):
    return is_admin(user) or user == event.organizer

# USER Model CRUD and Auth ---------> 

#sign-up user
def create_participant(request):
    participant_form=ParticipantModelForm()

    if request.method=='POST':
        participant_form=ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            user=participant_form.save(commit=False)
            # print(user)
            user.set_password(participant_form.cleaned_data.get('password1'))
            # user.is_active=False #uncomment this before deploy
            print(participant_form.cleaned_data)
            user.save()
            participant_form.save() #comment this before deploy
            messages.success(request,"A confirmation mail sent to your email. please check")
            return redirect('sign-in')
        else:
            messages.error(request,'Properly fill up the form!')
            return redirect('create-participant')

    context={
        'participant_form':participant_form,
        'form_title':'Register a New Participant'
    }
    return render(request,'registration/create_participant.html',context)

class UpdateProfile(UpdateView):
    model=User
    template_name='registration/create_participant.html'
    form_class=EditProfileForm
    context_object_name='form'
    pk_url_kwarg='id'
    success_url=reverse_lazy('user-profile')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['participant_form']=self.get_form()
        context['form_title']='Update Profile'
        return context





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
    form=CustomLoginForm()
    if request.method=='POST':
        form=CustomLoginForm(data=request.POST)
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

# GROUP Model CRUD --------> 

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method=='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f'Group {group.name} created successfully')
            return redirect('create-group')
    
    context={
        'form':form,
        'title':'Create New Group',
        'submit_text':'Create Group'
        }
    return render(request,'admin/create_group.html',context)


class GroupList(UserPassesTestMixin,ListView):
    model=Group
    template_name='admin/group_list.html'
    context_object_name='groups'

    def test_func(self):
        return is_admin(self.request.user)
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()

class UpdateGroup(UserPassesTestMixin,UpdateView):
    model=Group
    form_class=CreateGroupForm
    template_name='admin/create_group.html'
    pk_url_kwarg='group_id'
    success_url=reverse_lazy('group-list')
    context_object_name='form'

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Update Group'
        context['submit_text'] = 'Update'
        return context

    def form_valid(self, form):
        messages.success(self.request, "Group Updated Successfully!!!")
        return super().form_valid(form)
    



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
def delete_group(request,group_id):
    if request.method=='POST':
        group=Group.objects.get(id=group_id)
        group.delete()
        messages.success(request,'Group removed!!')
        return redirect('group-list')
    else:
        messages.error(request,'Group NOT removed')
        return redirect('group-list')

@login_required
def rsvp_to_events(request,event_id):
    if request.method =='POST':
        user=request.user
        event=Event.objects.get(id=event_id)
        if user.rsvp_events.filter(id=event_id).exists():
            user.rsvp_events.remove(event)
            messages.success(request,"You have un-registered from this event!!!")
            return redirect('user-dashboard')
        else:
            user.rsvp_events.add(event)
            messages.success(request,"Event successfully registered!!!")
            return redirect('user-dashboard')

# DASHBOARD MANAGEMENT ------------>
# dashboard Router
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
    group_count = Group.objects.all().count()
    category_count = Category.objects.all().count()
    
    if query_type=='participants':
        contents=User.objects.all()
    else:
        contents=Event.objects.prefetch_related('participants').all()
    
    context={
        'contents':contents,
        'group_count':group_count,
        'category_count':category_count
        }
    print('Admin Dashboard context: ',contents)
    return render(request,'admin/admin_dashboard.html',context)

def user_dashboard(request):
    user=request.user
    context={
        'user':user
        }
    return render(request,'dashboard/user_dashboard.html',context)

class OrganizerDashboard(ListView):
    model=Event
    template_name='dashboard/organizer_dashboard.html'
    context_object_name='events'
    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        query_type=self.request.GET.get('type')

        event_count=Event.objects.aggregate(
            total=Count(
                'id',
                filter=Q(organizer=self.request.user),
                distinct=True),
            upcoming=Count(
                'id',
                filter=Q(organizer=self.request.user,date__gt=date.today()),
                distinct=True),
            past=Count(
                'id',
                filter=Q(organizer=self.request.user,date__lt=date.today()),
                distinct=True),
            # unique_participants=Count('participants',distinct=True)
        ) 
        event_count['unique_participants'] = 7
        context['event_count']=event_count
        context['url_name']='organizer-dashboard'

        if query_type=='total':
            context['title']='Your Total Events'
        elif query_type=='upcoming':
            context['title']='Your Upcoming Events'
        elif query_type=='upcoming':
            context['title']='Your Upcoming Events'
        elif query_type=='past':
            context['title']='Your Past Events'
        else:
            context['title']='Your Todays Events'
        
        stats_cards = [
            {
                'title':'Total Participants',
                'count':event_count['unique_participants'],
                'type':'participants'
            },
            {
                'title':'Your Total Events',
                'count':event_count['total'],
                'type':'total'
            },
            {
                'title':'Your Upcoming Events',
                'count':event_count['upcoming'],
                'type':'upcoming'
            },
            {
                'title':'Your Past Events',
                'count':event_count['past'],
                'type':'past'
            }
        ]
        context['stats_cards'] = stats_cards
        return context
    
    def get_queryset(self):
        query_type=self.request.GET.get('type')
        events=Event.objects.select_related('category').prefetch_related('participants').filter(organizer=self.request.user)
        
        if query_type=='total':
            events=events.all()
        elif query_type=='upcoming':
            events=events.filter(date__gt=date.today())
        elif query_type=='past':
            events=events.filter(date__lt=date.today())
        else:
            upcomingEvents=Event.objects.filter(date__gt=date.today())
            events=events.filter(date__exact=date.today())
        return events

class ProfileView(TemplateView):
    template_name='accounts/profile.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context['member_since']=user.date_joined
        context['profile_image']=user.profile_image
        context['phone_number']=user.phone_number
        context['id']=user.id

        return context

# Password Change and Reset Views ------>

class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class=CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')

    #sending the email user 
	#receiving necessary data from url to send email to user
	#this context data will be sent to email_template (set by default)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'A reset email sent, please check your email')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request,'Password reset succefully')
        return super().form_valid(form)
from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.forms import EventModelForm,CategoryModelForm
from events.models import Event,Category
from django.contrib import messages
from datetime import date
from django.db.models import Q,Count
from django.contrib.auth.decorators import login_required,user_passes_test
from users.views import is_admin,is_organizer,admin_or_organizer
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse_lazy
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

class EventList(ListView):
    pass
    # events=Event.objects.select_related('category').prefetch_related('participants').all()
    # if request.method=="POST":
    #     search_value = request.POST.get('search')
    #     search_type = request.POST.get('search_type')
    #     print(search_value)
    #     print('Search Type: ', search_type)
    #     if search_type=="category":
    #         print('inside category search')
    #         events=events.filter(category__name__icontains=search_value)
    #     else:
    #         events=events.filter(name__icontains=search_value)
            
    # context={
    #     'events':events
    # }

@user_passes_test(admin_or_organizer,login_url='no-permission')
def create_category(request):
    category_form=CategoryModelForm()

    if request.method=='POST':
        category_form=CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,'Category created successfully!')
            context={
                'form':category_form,
                'title':'Create A New Category'
            }
            return redirect('create-category')
        else:
            messages.error(request,'Properly fill up the form!')
            return redirect('create-category')
    
    context={
        'form':category_form,
        'title':'Create A New Category'
        }
    return render(request,'create_category.html',context)

class UpdateCategory(UpdateView):
    model = Category
    form_class=CategoryModelForm
    pk_url_kwarg='category_id'
    context_object_name='form'
    template_name='create_category.html'
    success_url=reverse_lazy('create-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Category'
    #     current_obj = self.get_object()
    #     print(current_obj)
    #     context['category_form'] = CategoryModelForm(instance=current_obj)
        return context

    def form_valid(self, form):
        # category_name = form.cleaned_data.get('name')
        # does_exist = Category.objects.filter(name = category_name).exists()
        # if does_exist:
        #     messages.error(self.request,"Category with same name already exists")
        #     return render(self.request, 'create_category.html', self.get_context_data())
        messages.success(self.request,"Category Updated Successfully!!!")
        return super().form_valid(form)
    

class CategoryList(UserPassesTestMixin,ListView):
    model=Category
    template_name='admin/category_list.html'
    context_object_name='categories'


    def test_func(self):
        return is_admin(self.request.user)
    
    def get_queryset(self):
        return Category.objects.prefetch_related('event_list').all()

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







def show_details(request,id): #prefetch_related name replaced from 'participant_list'
    event=Event.objects.prefetch_related('participants').get(id=id)

    context={'event':event}

    return render(request,'event_details.html',context)
"""Event Details CBV hoy nai


class EventDetails(DetailView):
    model=Event
    context_object_name='event'
    template_name='event_details.html'
    # pk_url_kwarg='id'
    def get_queryset(self):
        # id=self.kwargs.get('id')
        event=self.get_object()
        print(event)
        print('event id: ',event.id)
        return Event.objects.prefetch_related('participants').get(id=event.id)
"""




class DeleteEvent(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    login_url='no-permission'
    model=Event
    pk_url_kwarg='id'
    success_url=reverse_lazy('dashboard')

    def test_func(self):
        return admin_or_organizer(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request,'Event deleted!!')
        return super().delete(request, *args, **kwargs)




class DeleteCategory(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model=Category
    login_url='no-permission'
    success_url=reverse_lazy('dashboard')
    pk_url_kwarg='id'

    def test_func(self):
        return admin_or_organizer(self.request.user)
    
    def delete(self,request,*args,**kwargs):
        messages.success(request,'Category deleted!!')
        return super().delete(request,*args,**kwargs)


    
    
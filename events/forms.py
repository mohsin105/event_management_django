from django import forms
from events.models import Event,Category
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User=get_user_model()

class EventModelForm(forms.ModelForm): #queryset e participant k user diye replace korsi. 
    participants=forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                widget=forms.CheckboxSelectMultiple,required=False)
    class Meta:
        model=Event
        fields=['name','description','date','time','location','category','participants','asset'] #,'participant_list' does not work

        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder': 'Enter Name',
                    'class':'border rounded-md p-1 my-2'
                    }),
            'description':forms.Textarea(
                attrs={
                    'class':'border border-gray-400  rounded-md p-1 my-2',
                    'placeholder': 'Description about the Event',
                    'rows':8
                    }),
            'date':forms.SelectDateWidget(
                attrs={
                    'class':'border rounded-md p-1 my-2',
                    
                    }),
            'time':forms.TimeInput(
                attrs={
                    'placeholder':'HH:MM:SS',
                    'class':'border',
                    'type':'time'
                    }),
            'location':forms.Textarea(
                attrs={
                    'class':'border border-3 p-1 rounded-md my-2',
                    'rows':3
                    }),
            'category':forms.Select(
                attrs={
                    'class':' display-block bg-black border border-3 rounded-md p-1 my-2',
                    }),
            'participants': forms.CheckboxSelectMultiple(
                attrs={
                    'class':'',
                }
            ),
        #  'category':forms.CheckboxSelectMultiple(attrs={'class':' display-block bg-black'})
            }
# 'category':forms.Select(attrs={'class':' display-block bg-black border border-3'})                 

# sign-up new participant user



class CategoryModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']

        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder': 'Category Name',
                    'class':'border p-2 my-4 rounded-md w-full',
                    }),
            'description':forms.Textarea(
                attrs={
                    'class':'border border-3 border-black p-2 my-4 rounded-md w-full',
                    'placeholder':'Desciption of the Category',
                    'rows':8
                    }),
        }
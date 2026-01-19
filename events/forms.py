from django import forms
from events.models import Event,Category
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User=get_user_model()

class EventModelForm(forms.ModelForm): #queryset e participant k user diye replace korsi. 
    participants=forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
        )
    class Meta:
        model=Event
        fields=['name','description','date','start_time','end_time','location','category','capacity','status','participants','asset'] #,'participant_list' does not work

        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder': 'Enter Name',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                    }),
            'description':forms.Textarea(
                attrs={
                    'class':'w-full my-2 p-4 border border-gray-400 rounded-md shadow-md',
                    'placeholder': 'Description about the Event',
                    'rows':8
                    }),
            'date':forms.DateInput(
                attrs={
                    'class':'w-1/2 p-4 my-2 border-2 border-gray-500 rounded-md shadow-md',
                    'type':'date'
                    }),
            'start_time':forms.TimeInput(
                attrs={
                    'placeholder':'HH:MM:SS',
                    'class':'w-1/3 p-4 my-2 border-2 border-gray-500 rounded-md shadow-md',
                    'type':'time'
                    }),
            'end_time':forms.TimeInput(
                attrs={
                    'class':'w-1/3 p-4 my-2 border-2 border-gray-500 rounded-md shadow-md',
                    'type':'time'
                }
            ),
            'location':forms.Textarea(
                attrs={
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md',
                    'rows':3
                    }),
            'category':forms.Select(
                attrs={
                    'class':'w-1/2 p-4 my-2 display-block bg-black border-2 border-gray-400  rounded-md ',
                    }),
            'capacity':forms.NumberInput(
                attrs={
                    'class':'w-1/6 p-4 my-2 border-2 border-gray-400 rounded-md shadow-md',
                    
                }
            ),
            'status':forms.Select(
                attrs={
                    'class':'w-1/3 p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            ),
            'participants': forms.CheckboxSelectMultiple(
                attrs={
                    'class':' p-4 my-2 flex border-2 border-gray-400 rounded-md',
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
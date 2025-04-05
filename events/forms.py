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

        widgets={'name':forms.TextInput(attrs={'placeholder': 'Enter Name','class':'border'}),
                 'description':forms.Textarea(attrs={'class':'border border-3'}),
                 'date':forms.SelectDateWidget(attrs={'class':'border'}),
                 'time':forms.TimeInput(attrs={'placeholder':'HH:MM:SS','class':'border'}),
                 'location':forms.Textarea(attrs={'class':'border border-3'}),'category':forms.Select(attrs={'class':' display-block bg-black border border-3'})
                #  'category':forms.CheckboxSelectMultiple(attrs={'class':' display-block bg-black'})
                 }
# 'category':forms.Select(attrs={'class':' display-block bg-black border border-3'})                 

# sign-up new participant user



class CategoryModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']

        widgets={
            'name':forms.TextInput(attrs={'placeholder': 'Enter Name','class':'border'}),
                             'description':forms.Textarea(attrs={'class':'border border-3'}),

        }
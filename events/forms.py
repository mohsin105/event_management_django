from django import forms
from events.models import Event,Participant,Category


class EventModelForm(forms.ModelForm):
    participants=forms.ModelMultipleChoiceField(queryset=Participant.objects.all(),
                                                widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Event
        fields=['name','description','date','time','location','category','participants'] #,'participant_list' does not work

        widgets={'name':forms.TextInput(attrs={'placeholder': 'Enter Name','class':'border'}),
                 'description':forms.Textarea(attrs={'class':'border border-3'}),
                 'date':forms.SelectDateWidget(attrs={'class':'border'}),
                 'time':forms.TimeInput(attrs={'placeholder':'HH:MM:SS','class':'border'}),
                 'location':forms.Textarea(attrs={'class':'border border-3'}),
                #  'category':forms.RadioSelect(attrs={'class':'border border-3'})
                 }
                 


class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['name','email','events']

        widgets={'events':forms.CheckboxSelectMultiple(attrs={'class':'border border-3'})}

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']

        widgets={
            'name':forms.TextInput(attrs={'placeholder': 'Enter Name','class':'border'}),
                             'description':forms.Textarea(attrs={'class':'border border-3'}),

        }
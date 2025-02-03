from django import forms
from events.models import Event,Participant,Category
class EventModelForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','description','date','time','location']


class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['name','email']

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']
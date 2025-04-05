from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
# Create your models here.

class Event(models.Model):
    name=models.CharField(max_length=300)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField() #(HH:MM:SS)
    location=models.TextField()
    category=models.ForeignKey('Category',on_delete=models.CASCADE,default=1,related_name='event_list')
    participants=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='rsvp_events',null=True,blank=True)
    asset=models.ImageField(upload_to='tasks_asset',blank=True,null=True,default='tasks_asset/default_img.jpg')
    def __str__(self):
        return self.name

# class Participant(models.Model):
#     name=models.CharField(max_length=250)
#     email=models.EmailField(unique=True)
#     events=models.ManyToManyField(Event,related_name='participant_list',null=True,blank=True)

#     def __str__(self):
#         return self.name

class Category(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.name

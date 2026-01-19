from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
# Create your models here.

class Event(models.Model):
    status_choices = (
        ('DRAFT','Draft'),
        ('PUBLISHED','Published'),
        ('POSTPONED','Postponed'),
        ('CANCELLED','Cancelled'),
        ('COMPLETED','Completed'),
    )
    name=models.CharField(max_length=300)
    description=models.TextField()
    date=models.DateField()
    start_time=models.TimeField() #(HH:MM:SS)
    end_time=models.TimeField(null=True, blank=True)
    location=models.TextField()
    category=models.ForeignKey('Category',on_delete=models.CASCADE,default=1,related_name='event_list')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,related_name='organized_events')
    participants=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='rsvp_events',null=True,blank=True)
    asset=models.ImageField(upload_to='tasks_asset',blank=True,null=True,default='tasks_asset/default_img.jpg')
    capacity = models.IntegerField(default=5, blank=True, null=True)
    status = models.CharField(max_length=15, choices=status_choices, default='PUBLISHED')
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.name

# class Participant(models.Model):
#     name=models.CharField(max_length=250)
#     email=models.EmailField(unique=True)
#     events=models.ManyToManyField(Event,related_name='participant_list',null=True,blank=True)

#     def __str__(self):
#         return self.name

class Category(models.Model):
    name=models.CharField(max_length=200, unique=True)
    description=models.TextField()

    def __str__(self):
        return self.name

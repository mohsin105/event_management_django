from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_image=models.ImageField(upload_to='profile_images',blank=True,default='profile_images/default.jpg')
    phone_number=models.CharField(max_length=18)

    # phone number validation korte hobe

    def __str__(self):
        return self.username
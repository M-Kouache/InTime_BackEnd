from django.db import models
from django.contrib.auth.models import AbstractUser
from events.models import Service

class User(AbstractUser):
    password = models.CharField(max_length=255,unique=True,blank=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150,unique=True,blank=False)
    last_name = models.CharField(max_length=150,unique=True,blank=False)



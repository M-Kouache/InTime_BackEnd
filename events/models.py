from django.db import models
from django.conf import settings


class Department(models.Model):
    libelle = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.libelle

    class Meta:
        ordering = ['id']


class Service(models.Model):
    libelle = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,default=1)

    def __str__(self) -> str:
        return self.libelle

    class Meta:
        ordering = ['id']

class UserProfile(models.Model):
    service = models.ForeignKey(Service,default=1,on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

class Handler(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owner')
    user_handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_handler')


class Events(models.Model):
    date_start = models.DateTimeField(auto_now_add=False)
    date_end = models.DateTimeField(auto_now_add=False)
    public_events = models.BooleanField(default=True)
    departement = models.ForeignKey(Department, on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=50,default="No Title")
    description = models.TextField(null=True)
    location = models.CharField(max_length=100,null=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='actor')


class Reciever(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class E_Notification(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    notifier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)
    is_administrateur = models.BooleanField(default=False)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='Client_images',null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

class Organizer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(upload_to='Organizer_images',null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    website = models.URLField(blank=True,null=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
       return "Organizer Name : "+self.user.first_name
   



class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Events_images',null=True,blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    first_class_price = models.DecimalField(max_digits=8, decimal_places=2)
    second_class_price = models.DecimalField(max_digits=8, decimal_places=2)
    third_class_price = models.DecimalField(max_digits=8, decimal_places=2)

    objects = models.Manager()

    def __str__(self):
       return "Event Title : "+self.title
    
class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    objects = models.Manager()

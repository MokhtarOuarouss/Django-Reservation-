from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.


class User(AbstractUser):
    is_client = models.BooleanField(default=True)
    is_organizer = models.BooleanField(default=False)
    is_administrateur = models.BooleanField(default=False)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='Client_images', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='Organizer_images', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return "Organizer Name : " + self.user.first_name


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='administrator/profile', default='Default/user.png')

    objects = models.Manager()

    def __str__(self):
        return "Administrator Name : " + self.user.first_name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Events_images', null=True, blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    first_class_price = models.DecimalField(max_digits=8, decimal_places=2)
    second_class_price = models.DecimalField(max_digits=8, decimal_places=2)
    third_class_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_valid = models.BooleanField(default=False, null=True)
    status =  models.CharField(max_length=100,default='not-valid', null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return "Event Title : " + self.title


class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  null=True)  # Replace '1' with the appropriate default client ID
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)

    objects = models.Manager()

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    reservations = models.ManyToManyField(Reservation)
    
    objects = models.Manager()

class Notification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    objects = models.Manager()


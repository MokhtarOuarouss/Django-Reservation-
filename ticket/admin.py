from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Organizer)
admin.site.register(Administrator)
admin.site.register(Event)
admin.site.register(Reservation)
admin.site.register(Notification)


from django.contrib import admin
from django.urls import path
from . import views
app_name = 'ticket'

urlpatterns = [
    
    path('', views.Event_List, name='event_list'),
    #path('contact', views.d_contact, name='d_contact'),
    #path('contact', views.contact_form, name='f_contact'),
    path('signup', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('profil/', views.Profil, name='profil'),
    path('Organizer', views.espace_organizer, name='Organizer'),
    path('Client', views.espace_client, name='Client'),
    path('admin', views.espace_admin, name='admin'),

    # path('<slug:slug>/', views.post_detail, name='post_detail'),
   # path('Events', views.Event_List, name='event_list')
]

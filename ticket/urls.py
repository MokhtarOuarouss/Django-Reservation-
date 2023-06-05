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
    path('a_admin', views.espace_admin, name='a_admin'),
    path('Logout',views.Logout, name="Logout"),
    path('profil/updateProfil', views.updateProfil, name='updateprofil'),
    path('profil/AddEvents', views.AddEvents, name='AddEvents'),
    path('profil/updateImageProfil', views.updateImageProfil, name='updateImageProfil'),
    path('profil/UpdateEvents/<int:id>', views.UpdateEvents, name='UpdateEvents'),
    path('profil/DeleteEvent/<int:id>', views.DeleteEvent, name='DeleteEvent'),
    path('profil/Events', views.Event_List_organizer, name='Event_List_organizer'),
    path('organizer/OrganizerInfo/<int:id>', views.OrganizerInfo, name='OrganizerInfo'),
    path('organizer/EventrInfo/<int:id>', views.EventrInfo, name='EventrInfo'),
    path('/Search', views.Search, name='Search'),
    # path('<slug:slug>/', views.post_detail, name='post_detail'),
   # path('Events', views.Event_List, name='event_list')
]

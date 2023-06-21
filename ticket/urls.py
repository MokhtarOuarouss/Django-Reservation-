from django.contrib import admin
from django.urls import path, register_converter
from . import views

app_name = 'ticket'


class DecimalConverter:
    regex = r'[-+]?\d*\.\d+|\d+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)


register_converter(DecimalConverter, 'decimal')  # Register the custom converter

urlpatterns = [

    path('', views.Event_List, name='event_list'),
    # path('contact', views.d_contact, name='d_contact'),
    # path('contact', views.contact_form, name='f_contact'),
    path('signup', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('Logout', views.Logout, name="Logout"),

    path('Client', views.espace_client, name='espace_client'),
    path('Client/updateProfil', views.ClientupdateProfil, name='ClientupdateProfil'),
    path('Client/AddReservation/<int:id>/<decimal:price>/', views.AddReservation, name='AddReservation'),
    path('Client/updatePrice/<int:id>/<decimal:price>/', views.updatePrice, name='updatePrice'),
    path('Client/updateQuantity/<int:id>', views.updateQuantity, name='updateQuantity'),
    path('Client/Deletereservation/<int:id>', views.Deletereservation, name='Deletereservation'),
    path('Client/Cart', views.Cart, name='Cart'),
    path('Search/', views.Search, name='Search'),
    path('Search/<str:search>/', views.SearchByCategory, name='SearchByCategory'),


    path('profil/', views.Profil, name='profil'),
    path('Organizer', views.espace_organizer, name='Organizer'),
    path('profil/updateprofil', views.updateprofil, name='updateprofil'),
    path('profil/AddEvents', views.AddEvents, name='AddEvents'),
    path('profil/updateImageProfil', views.updateImageProfil, name='updateImageProfil'),
    path('profil/UpdateEvents/<int:id>', views.UpdateEvents, name='UpdateEvents'),
    path('profil/DeleteEvent/<int:id>', views.DeleteEvent, name='DeleteEvent'),
    path('profil/Events', views.Event_List_organizer, name='Event_List_organizer'),
    path('organizer/OrganizerInfo/<int:id>', views.OrganizerInfo, name='OrganizerInfo'),
    path('organizer/EventrInfo/<int:id>', views.EventrInfo, name='EventrInfo'),
    

    path('administrator', views.espace_admin, name='administrateur'),
    path('administrator/events/', views.admin_event, name='AdminEvent'),
    path('administrator/events/validation/event/<int:idk>/', views.Valider_Event, name='EventValid'),
    path('administrator/Clients/', views.client_admin, name='AdminClient'),
    path('administrator/Organizers/', views.Organizer_admin, name='AdminOrganizer'),
    path('administrator/Notification/New/', views.read_notification, name='Notifications'),
    path('administrator/Notification/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('administrator/EventrInfo/<int:id>', views.EventInfo_byAdmin, name='EventInfo_byAdmin'),

]









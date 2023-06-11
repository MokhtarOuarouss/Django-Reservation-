from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import *
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request,'index.html')
#Show Event where is_valid = True
def Event_List(request):
    context = {'Events': Event.objects.filter(is_valid=True)}
    return render(request, 'Events.html', context)

#Search by title and by city
def Search(request):
    query = request.GET.get('search')  # Get the search query from the request

    if query:
         results = Event.objects.filter(Q(title__icontains=query) | Q(city__icontains=query) ,is_valid=True)
          # Perform the search using the 'icontains' lookup
    else:
        results = Event.objects.none()  # Empty queryset when no search query is provided
    return render(request, 'Events.html', {'Events': results, 'query': query})



#ORGANIZER 


def signup(request):
    if request.method == 'POST':
        nom = request.POST.get('Nom')
        prenom = request.POST.get('Prenom')
        email = request.POST.get('Email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        type = request.POST.get('type')

        # Vérification de la validité des données
        if password != password1:
            return redirect('ticket:signup')
        if not nom or not prenom or not email or not password or not password1:
            return redirect('ticket:signup')
        if User.objects.filter(email=email):
            return redirect('ticket:signup')
        # Rediriger l'utilisateur vers une page de confirmation
        else:
            utilisateur = User.objects.create_user(username=email, email=email, password=password,
                                                   first_name=prenom,
                                                   last_name=nom)
            users = authenticate(request, username=email, password=password)
            login(request, users)
            if type == 'organizer':
                utilisateur.is_organizer=True
                utilisateur.is_client=False
                organizer = Organizer.objects.create(user=utilisateur)
                organizer.save()
                utilisateur.save()
                return redirect('ticket:profil')
            elif type == 'client':
                utilisateur.is_client = True
                client = Client.objects.create(user=utilisateur)
                client.save()
                utilisateur.save()
                return redirect('ticket:espace_client')
    return render(request, 'Inscription.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_client:
                return redirect('ticket:espace_client')
            elif user.is_organizer:
                return redirect('ticket:profil')
            else:
                return redirect('ticket:administrateur')
    return render(request, 'Login.html')
@login_required(login_url="/signin")
def Logout(request):
    logout(request)
    return redirect('ticket:signin')


"""---------------------Organizer------------------"""

@login_required(login_url="/signin")
def Profil(request):
    user = request.user
    organizer = Organizer.objects.filter(user=user).first()
    events = Event.objects.filter(organizer=organizer)
    context = {'organizer': organizer, 'Events': events}
    return render(request, 'profil.html', context)

@login_required(login_url="/signin")
def updateProfil(request):
    if request.method == 'POST':
        user = request.user
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        phoneNumber = request.POST.get('phone_number')
        company = request.POST.get('company_name')
        address = request.POST.get('address')
        website = request.POST.get('website')

        organizer = Organizer.objects.filter(user=user).first()
        user.first_name = firstname
        user.last_name = lastname
        organizer.phone_number = phoneNumber
        organizer.address = address
        organizer.website = website
        organizer.company_name = company

        user.save()
        organizer.save()

        return redirect("ticket:profil")

def updateImageProfil(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        user = request.user
        organizer = Organizer.objects.filter(user=user).first()

        if image is not None:
            organizer.image = image
        
        organizer.save()
        
    return redirect("ticket:profil")

@login_required(login_url="/signin")
def AddEvents(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        date_string = request.POST.get('date')
        location = request.POST.get('location')
        city = request.POST.get('city')
        type = request.POST.get('type')
        firstprice = request.POST.get('firstprice')
        secondprice = request.POST.get('secondprice')
        thirsprice = request.POST.get('thirsprice')
        description = request.POST.get('description')

        date, time = date_string.split('T')
        organizer = Organizer.objects.filter(user=user).first()
        image = request.FILES.get('image')

        # event = Event.objects.filter(organizer=organizer).first()

        event = Event.objects.create(title=title,
                                     date=date,
                                     time=time,
                                     location=location,
                                     city=city,
                                     type=type,
                                     first_class_price=firstprice,
                                     second_class_price=secondprice,
                                     third_class_price=thirsprice,
                                     description=description,
                                     image=image,
                                     organizer=organizer)

        event.save()
        msg = organizer.user.first_name + ' ' + organizer.user.last_name + ' has submitted a new event. Title: ' + title
        notification = Notification.objects.create(message=msg, event=event, organizer=organizer)
        notification.save()
        return redirect("ticket:profil")


def UpdateEvents(request, id):
    if request.method == 'POST':
        user = request.user
        organizer = Organizer.objects.filter(user=user).first()
        event = Event.objects.get(id=id)
        title = request.POST.get('title')
        date_string = request.POST.get('date')
        location = request.POST.get('location')
        city = request.POST.get('city')
        type = request.POST.get('type')
        firstprice = request.POST.get('firstprice')
        secondprice = request.POST.get('secondprice')
        thirsprice = request.POST.get('thirsprice')
        description = request.POST.get('description')

        date, time = date_string.split('T')
        # event = Event.objects.filter(organizer=organizer).first()

        event.title = title
        event.date = date
        event.time = time
        event.location = location
        event.type = type
        event.city = city
        event.first_class_price = firstprice
        event.second_class_price = secondprice
        event.third_class_price = thirsprice
        event.description = description

        image = request.FILES.get('image')
        if image is not None:
            # Process the uploaded file
            event.image = image
        event.save()

        msg = organizer.user.first_name + ' ' + organizer.user.last_name + ' has updated an event. Title: ' + title
        notification = Notification.objects.create(message=msg, event=event, organizer=organizer)
        notification.save()
        return redirect('ticket:profil')


def DeleteEvent(request, id):
    user = request.user
    organizer = Organizer.objects.filter(user=user).first()
    event = Event.objects.get(id=id)
    msg = organizer.user.first_name + ' ' + organizer.user.last_name + ' has updated an event. Title: ' + event.title
    notification = Notification.objects.create(message=msg, organizer=organizer)
    notification.save()
    event.delete()

    return redirect('ticket:Event_List_organizer')
        
def DeleteEvent(request,id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('ticket:Event_List_organizer')

def Event_List_organizer(request):
    user = request.user
    organizer = Organizer.objects.filter(user=user).first()
    events = Event.objects.filter(organizer=organizer)
    context = {'Events': events}
    return render(request, 'EventByErg.html', context)


def OrganizerInfo(request, id):
    organizer = Organizer.objects.get(id=id)
    events = Event.objects.filter(organizer=organizer)
    context = {'Organizer': organizer, 'Events': events}

    return render(request, 'OrganizerInfo.html', context)

def EventrInfo(request, id):
    event = Event.objects.get(id=id)
    context = { 'event': event}
    return render(request, 'Eventinfo.html', context)

def espace_organizer(request):
    user = request.user
    org = Organizer.objects.filter(user=user).first()
    return render(request, 'Organizer/index.html', {'org': org})


"""----------------Clients------------------ """
@login_required(login_url="/signin")
def espace_client(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    return render(request, 'Clients/clientInfo.html',{'client': client})

def ClientupdateProfil(request):
    if request.method == 'POST' :
        user = request.user
        Firstname = request.POST.get('first_name')
        Lastname = request.POST.get('last_name')
        PhoneNumber = request.POST.get('phone_number')
        
        address = request.POST.get('address')

        client = Client.objects.filter(user=user).first()
        user.first_name = Firstname
        user.last_name = Lastname
        client.phone_number = PhoneNumber
        client.address = address

        image = request.FILES.get('image')
        
        if image is not None:
            # Process the uploaded file
            #client.image.delete()
            client.image = image
        """
        if isinstance(image, InMemoryUploadedFile):
            client.image.save(image.name,image)
        """
        user.save()
        client.save()

        return redirect("ticket:espace_client")


def AddReservation(request, id, price):
    if request.method == 'POST':
        user = request.user
        client = Client.objects.filter(user=user).first()
        event = Event.objects.filter(id=id).first()

        reservation = Reservation.objects.create(client=client, event=event, price=price)
        reservation.save()

        return redirect("/")


def Cart(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    reservations = Reservation.objects.filter(client=client)

    total = 0
    for reservation in reservations:
        sub_total = reservation.quantity * reservation.price
        reservation.sub_total = sub_total
        total += sub_total

    context = {'Reservation': reservations, 'total': total}

    return render(request, 'Clients/Cart.html', context)


def updatePrice(request, id, price):
    if request.method == 'POST':
        reservation = Reservation.objects.filter(id=id).first()

        reservation.price = price
        reservation.save()

        return redirect("/Client/Cart")


def updateQuantity(request, id):
    if request.method == 'POST':
        reservation = Reservation.objects.filter(id=id).first()
        quantity = int(request.POST.get('quantity', 1))
        reservation.quantity = quantity
        reservation.save()

        return redirect("/Client/Cart")


def Deletereservation(request, id):
    reservation = Reservation.objects.get(id=id)
    reservation.delete()
    return redirect("/Client/Cart")


"""----------------Administrator------------"""
@login_required(login_url="/signin")
def espace_admin(request):
    user = request.user
    admin = Administrator.objects.get(user=user)
    event_count=Event.objects.count()
    organizer_count=Organizer.objects.count()
    client_count=Client.objects.count()
    notification_count = Notification.objects.filter(is_read=False).count()
    sport_count = Event.objects.filter(type='Sports').count()
    training_programs_count = Event.objects.filter(type='Training Programs').count()
    networking_count = Event.objects.filter(type='Networking Events').count()
    music_count = Event.objects.filter(type='Music').count()
    festivals_count = Event.objects.filter(type='Festivals/Celebrations').count()
    context={'event_count': event_count,
             'organizer_count': organizer_count,
             'client_count': client_count,
             'count': notification_count,
             'admin': admin,
             'sport_count': sport_count,
             'training_programs_count': training_programs_count,
             'networking_count': networking_count,
             'music_count': music_count,
             'festivals_count': festivals_count,
    }
    return render(request, 'Administrateur/index.html', context)

def admin_event(request):
    event = Event.objects.all()
    notification_count = Notification.objects.filter(is_read=False).count()

    return render(request, 'Administrateur/Events.html', {'Events': event, 'count': notification_count})

def Valider_Event(request,idk):
    event = Event.objects.get(id=idk)
    if event.is_valid:
        messages.info(request, 'Event ' + event.title + ' déja  valider ')
    else:
        event.is_valid = True
        messages.info(request, 'Event ' + event.title + ' is valid successfully ')
    event.save()
    return redirect('ticket:AdminEvent')

def client_admin(request):
    client = Client.objects.all()
    paginator = Paginator(client, per_page=9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification_count = Notification.objects.filter(is_read=False).count()
    return render(request,'Administrateur/Client.html', {'clients': page_obj, 'count':notification_count})

def Organizer_admin(request):
    organizer = Organizer.objects.all()
    paginator = Paginator(organizer, per_page=9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notification_count = Notification.objects.filter(is_read=False).count()
    return render(request, 'Administrateur/Organizer.html', {'organizers': page_obj, 'count': notification_count})

def read_notification(request):
    notification = Notification.objects.all()
    for notification in notification:
        notification.is_read=True
        notification.save()
    notification = Notification.objects.all()
    return render(request, 'Administrateur/Notification.html', {'notifications': notification})
def delete_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.delete()
    return redirect('ticket:Notifications')
def base(request):

    return render(request, 'base.html')
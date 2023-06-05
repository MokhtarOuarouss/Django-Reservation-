from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from pyexpat.errors import messages

from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def Event_List(request):
    context = {'Events': Event.objects.all()}
    return render(request, 'Events.html', context)

def Search(request):
    query = request.GET.get('search')  # Get the search query from the request

    if query:
        results = Event.objects.filter(title__icontains=query)  # Perform the search using the 'icontains' lookup
    else:
        results = Event.objects.none()  # Empty queryset when no search query is provided

    return render(request, 'Events.html', {'Events': results, 'query': query})

@login_required(login_url="/signin")
def Profil(request):
    user = request.user
    organizer = Organizer.objects.filter(user=user).first()
    events = Event.objects.filter(organizer=organizer)
    context = {'organizer': organizer, 'Events': events}
    return render(request, 'profil.html', context)

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
            return redirect('ticket:signup/')
        if User.objects.filter(email=email):
            return redirect('ticket:signup')
        # Rediriger l'utilisateur vers une page de confirmation
        else:
            utilisateur = User.objects.create_user(username=email, email=email, password=password,
                                                   first_name=prenom,
                                                   last_name=nom)
            user = authenticate(request, username=email, password=password)
            login(request, user)
            if type == 'organizer':
                user.is_organizer = True
                organizer = Organizer.objects.create(user=user)
                organizer.save()
                utilisateur.save()
                return redirect('ticket:profil/')
            elif type == 'client':
                user.is_client = True
                client = Client.objects.create(user=user)
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
                return redirect('ticket:a_admin')
    return render(request, 'Login.html')
@login_required(login_url="/signin")
def Logout(request):
    logout(request)
    return redirect('ticket:signin')

@login_required(login_url="/signin")
def update(request):
    pass
@login_required(login_url="/signin")
def delete(request):
    pass

"""Organizer"""
@login_required(login_url="/signin")
def updateProfil(request):
    if request.method == 'POST':
        user = request.user
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        #email = request.POST.get('email')
        phoneNumber = request.POST.get('phone_number')
        company = request.POST.get('company_name')
        address = request.POST.get('address')
        website = request.POST.get('website')

        organizer = Organizer.objects.filter(user=user).first()
        user.first_name = firstname
        user.last_name = lastname
        #user.email = email
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

        if image:
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
        type = request.POST.get('type')
        firstprice = request.POST.get('firstprice')
        secondprice = request.POST.get('secondprice')
        thirsprice = request.POST.get('thirsprice')
        description = request.POST.get('description')
        
        date, time = date_string.split('T')
        organizer = Organizer.objects.filter(user=user).first()
        image =request.FILES.get('image')
        #event = Event.objects.filter(organizer=organizer).first()


        event = Event.objects.create(title=title,
                                     date=date,
                                     time=time,
                                     location=location,
                                     type= type,
                                     first_class_price=firstprice,
                                     second_class_price=secondprice,
                                     third_class_price=thirsprice,
                                     description=description,
                                     image= image,
                                     organizer=organizer)

        
        event.save()

        return redirect("ticket:profil")

def UpdateEvents(request,id):
    if request.method == 'POST':
        user = request.user
        event = Event.objects.get(id=id)
        title = request.POST.get('title')
        date_string = request.POST.get('date')
        location = request.POST.get('location')
        type = request.POST.get('type')
        firstprice = request.POST.get('firstprice')
        secondprice = request.POST.get('secondprice')
        thirsprice = request.POST.get('thirsprice')
        description = request.POST.get('description')
        
        date, time = date_string.split('T')
        image =request.FILES.get('image')
        #event = Event.objects.filter(organizer=organizer).first()


        event.title=title
        event.date=date
        event.time=time
        event.location=location
        event.type= type
        event.first_class_price=firstprice
        event.second_class_price=secondprice
        event.third_class_price=thirsprice
        event.description=description

        image = request.FILES.get('image')
        if image is not None:
            # Process the uploaded file
            event.image = image
        event.save()
        return redirect('ticket:profil')
        
def DeleteEvent(id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('ticket:profil')
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


"""Clients """
@login_required(login_url="/signin")
def espace_client(request):
    user = request.user
    client = Client.objects.filter(user=user).first()
    return render(request, 'Clients/clientInfo.html',{'client': client})

def ClientupdateProfil(request):
    if request.method == 'POST':
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
            client.image = image

        user.save()
        client.save()

        return redirect("ticket:espace_client")
"""Admin"""
@login_required(login_url="/signin")
def espace_admin(request):

    return render(request, 'Admin/index.html')
def base(request):

    return render(request, 'base.html')
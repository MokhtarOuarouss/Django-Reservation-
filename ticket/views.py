from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from pyexpat.errors import messages

from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def Event_List(request):

    #user = request.user
    #org = Organizer.objects.filter(user=user).first()
    context = {'Events': Event.objects.all()}
    return render(request, 'Events.html', context)

@login_required(login_url="/signin")
def Profil(request):

    context={'Events':Event.objects.all()}
    return render(request,'profil.html',context)

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
                return redirect('ticket:Client')
    return render(request, 'Inscription.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_client:
                return redirect('ticket:Client')
            elif user.is_organizer:
                return redirect('ticket:profil')
            else:
                return redirect('ticket:admin')
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
def espace_organizer(request):
    user = request.user
    org = Organizer.objects.filter(user=user).first()
    return render(request, 'Organizer/index.html', {'org': org})
"""Clients """
@login_required(login_url="/signin")
def espace_client(request):

    return render(request, 'Clients/index.html')
"""Admin"""
@login_required(login_url="/signin")
def espace_admin(request):

    return render(request, 'Admin/index.html')
def base(request):

    return render(request, 'base.html')
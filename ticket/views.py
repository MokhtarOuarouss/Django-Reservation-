from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from pyexpat.errors import messages

from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def Event_List(request):
    #context={'Events':Event.objects.all()}
    return render(request,'Events.html')

def Inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('Nom')
        prenom = request.POST.get('Prenom')
        email = request.POST.get('Email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Vérification de la validité des données
        if password != password1:
            pass
        if not nom or not prenom or not email or not password or not password1:
            pass
        if User.objects.filter(email=email):
            pass
        # Rediriger l'utilisateur vers une page de confirmation
        else:
            utilisateur = User.objects.create_user(username=email, email=email, password=password,
                                                   first_name=prenom,
                                                   last_name=nom)
            user = authenticate(request, username=email, password=password)
            login(request, user)
            utilisateur.save()

    pass

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Bienvenu')
            return redirect('Etudiant')
        else:
            messages.error(request, "erreur d'authentification")
    return render(request, 'Etudiant/Login.html')
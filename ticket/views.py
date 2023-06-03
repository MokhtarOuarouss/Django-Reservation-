from django.shortcuts import render,redirect

# Create your views here.

def Event_List(request):
    #context={'Events':Event.objects.all()}
    return render(request,'Events.html')
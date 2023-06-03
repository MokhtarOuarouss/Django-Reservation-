from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request,'index.html')

def Event_List(request):
    #context={'Events':Event.objects.all()}
    return render(request,'Events.html')
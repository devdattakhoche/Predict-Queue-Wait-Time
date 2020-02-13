from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    return render(request,'../templates/loginFolder/login.html')

def registration(request):
    if request.method=='POST':
        name = request.POST.get('Hospital_name')
        password = request.POST.get('password')
        user = User.objects.create_user(username=name,password=password)
        print(name,password)
    return render(request,'../templates/loginFolder/registration.html')
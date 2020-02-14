from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Pages.models import Hospital,Dept
from django.core.files.storage import FileSystemStorage

def index(request):
    if request.method=='POST':
        Hospital_id = Hospital.objects.get(Hospital_name=request.user.username)
        for i in range(1,int(request.POST['srajan1'])):
            Department_number = request.POST['Department[{}][number]'.format(i)]
            Department_name = request.POST['Department[{}][name]'.format(i)]
            Dept_instance = Dept.objects.create(Uid=Department_number,Type=Department_name,Hospital_id=Hospital_id)
    return render(request,'loginFolder/index.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('login'))

def login(request):
    if request.method == 'POST':
        name = request.POST.get('Hospital_name')
        password = request.POST.get('password')
        user = authenticate(username=name,password=password)
        if user:
            if user.is_active:
                auth_login(request,user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            
    return render(request,'loginFolder/login.html')

def registration(request):
    if request.method=='POST':
        name = request.POST.get('Hospital_name')
        password = request.POST.get('password')
        image = request.POST.get('image123')

        print(request.FILES)

        user = User.objects.create_user(username=name,password=password)
        print(name,password,image)
        hospital_instance = Hospital.objects.create(Hospital_name=name)
        return redirect(reverse('login'))
    return render(request,'loginFolder/registration.html')

@login_required
def department_delete(request):
    Hospital_id = Hospital.objects.get(Hospital_name=request.user.username)
    x = Dept.objects.filter(Hospital_id=Hospital_id)
    print(Hospital_id)
    params = {'dept':x,'hospital_id':Hospital_id}
    if request.method == 'POST':
        print(request.POST['hidden'])
        y = Dept.objects.get(Uid=request.POST['hidden'])
        y.delete()
        return render(request,'loginFolder/delete.html',params)

    return render(request,'loginFolder/delete.html',params)

@login_required
def department_update(request):
    if request.method == 'POST':
        x = Dept.objects.get(Uid=request.POST['hidden'])
        x.Uid = request.POST['number']
        x.Type = request.POST['name']
        x.save()

    Hospital_id = Hospital.objects.get(Hospital_name=request.user.username)
    x = Dept.objects.filter(Hospital_id=Hospital_id)
    params = {'dept':x,'hospital_id':Hospital_id}
    
    return redirect(reverse('view'))

@login_required
def update_form(request,slug):
    return render(request,'loginFolder/update_form.html',{'slug':slug})

@login_required
def view_department(request):
    Hospital_id = Hospital.objects.get(Hospital_name=request.user.username)
    x = Dept.objects.filter(Hospital_id=Hospital_id)
    
    params = {'dept':x,'hospital_id':Hospital_id}
    if 'form_rejected' in request.POST and request.method == "POST":
        # print(reverse('update_form',args=request.POST['object_id']))
        print(request.POST['object_id'])
        y = Dept.objects.get(Uid=request.POST['object_id'])
        y.delete()
        return render(request,'loginFolder/department.html',params)
    if 'form_approved' in request.POST and request.method == "POST":
        
        return redirect(reverse('update_form',args=[request.POST['object_id']]))
    return render(request, 'loginFolder/department.html',params)
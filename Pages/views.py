from django.shortcuts import render
from django.shortcuts import redirect
from .models import Dept,Hospital

def Documentation(request):
    return render(request,'Pages/Documentation.html')

def Single(request):
    x=Dept.objects.all()
    y = Dept.objects.get(Uid=1)
    print(y.image)  
    params={'Pro':x}
    if request.method== "POST" :
        No=request.POST.get('Dept_id')
        return redirect('/Dept/UID='+No)
    return render(request,'Pages/Single.html',params)

def Complete(request):
    return render(request,'Pages/Complete.html')

def Unknown(request):
    return render(request,'Pages/Unknown.html')
    
def Department(request,UID):
    x=Dept.objects.get(Uid=UID)
    params={'Pro':x}
    return render(request,'Pages/Department.html',params)

def Hospitals(request):
    x = Hospital.objects.all()
    params={'Pro':x}
    if request.method== "POST" :
        No=request.POST.get('Hospital_id')
        return redirect('/Single_hospital/'+No)
    return render(request,'Pages/Hospitals.html',params)

def Single_hospital(request,Hospital_id):
    x=Hospital.objects.get(Hospital_id=Hospital_id)
    params={'Pro':x}
    return render(request,'Pages/Single_hospital.html',params)
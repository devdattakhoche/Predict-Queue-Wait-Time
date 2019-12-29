from django.shortcuts import render
from django.shortcuts import redirect
from .models import Dept,Hospital

def Documentation(request):
    return render(request,'Pages/Documentation.html')
    
def Hospitals(request):
    x = Hospital.objects.all()  
    params={'Pro':x}
    if request.method== "POST" :
        No=request.POST.get('Hospital_id')
        return redirect('http://localhost:8000/Hospital/'+No+'/Dashboard')
    return render(request,'Pages/Hospitals.html',params)

def Dashboard(request,Hospital_id):
    x=Hospital.objects.get(Hospital_id=Hospital_id)
    params={'HosId_id':x}
    return render(  request,'Pages/Dashboard.html',params)

def Single(request,Hospital_id):
    a=Hospital.objects.get(Hospital_id=Hospital_id)
    x=Dept.objects.all()

    DepartmentList = []

    for i in x:
        DepartmentDict = {}
        DepartmentDict['Uid'] = str(i.Uid) 
        DepartmentDict['Type'] = str(i.Type)
        DepartmentDict['Image'] = i.image
        DepartmentDict['Hospital_id'] = str(i.Hospital_id)
        DepartmentList.append(DepartmentDict)

    params={'Pro':DepartmentList,'HosId':Hospital_id,'HosId_id':a}
    if request.method== "POST" :
        No=request.POST.get('Dept_id') 
        return redirect('http://localhost:8000/Hospital/'+Hospital_id+'/Dept/' + No)
    return render(request,'Pages/Single.html',params)

def Complete(request,Hospital_id):
    x=Hospital.objects.get(Hospital_id=Hospital_id)
    params={'HosId_id':x}
    return render(request,'Pages/Complete.html',params)

def Unknown(request,Hospital_id):
    x=Hospital.objects.get(Hospital_id=Hospital_id)
    params={'HosId_id':x}
    return render(request,'Pages/Unknown.html',params)
    
def Department(request,Hospital_id,UID):
    a = Hospital.objects.get(Hospital_id=Hospital_id)
    x = Dept.objects.all()
    y = Hospital.objects.all()
    
    DepartmentList = []
    HospitalList = []

    for i in x:
        DepartmentDict = {}
        DepartmentDict['Uid'] = str(i.Uid) 
        DepartmentDict['Type'] = str(i.Type)
        DepartmentDict['Hospital_id'] = str(i.Hospital_id)
        DepartmentList.append(DepartmentDict)

    for i in y:
        HospitalDict = {}
        HospitalDict['Hospital_name'] = str(i.Hospital_name) 
        HospitalDict['Hospital_id'] = str(i.Hospital_id)
        HospitalList.append(HospitalDict)

    params={'Pro':DepartmentList,'Hos':HospitalList,'ProId':UID,'HosId':Hospital_id,'HosId_id':a}
    return render(request,'Pages/Department.html',params)

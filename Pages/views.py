from django.shortcuts import render
from django.shortcuts import redirect
from .models import Dept,Hospital
from .filter import HospitalFilter
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pandas as pd
import pickle
import os
from django.conf import settings



def Documentation(request):
    return render(request,'Pages/Documentation.html')
    
def Hospitals(request):
    x = Hospital.objects.all()      
    Hospital_filter = HospitalFilter(request.GET,queryset=x)
    # HospitalFilter(request.GET).data['Hospital_name'].upper()
    params={'Pro':x,'filter':Hospital_filter}
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
        return redirect('/Hospital/'+Hospital_id+'/Dept/' + No)
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
    
def Train(request):
    iris = datasets.load_iris()
    data=pd.DataFrame({
        'sepal length':iris.data[:,0],
        'sepal width':iris.data[:,1],
        'petal length':iris.data[:,2],
        'petal width':iris.data[:,3],
        'species':iris.target
    })
    X=data[['sepal length', 'sepal width', 'petal length', 'petal width']]  # Features
    y=data['species']  # Labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    clf=RandomForestClassifier(n_estimators=100)
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred)*100)

    path = os.path.join(settings.MODEL_ROOT, 'clf')
    with open(path, 'wb') as file:
        pickle.dump(clf, file)

    return render(request,'Pages/sucess.html')


def Predict(request):
    z=None
    params = { 'pro': z }
    if request.method == "POST":
        First=request.POST.get('First')
        Second=request.POST.get('Second')
        Third=request.POST.get('Third') 
        Fourth=request.POST.get('Fourth')

        path = os.path.join(settings.MODEL_ROOT, 'clf')
        with open(path, 'rb') as file:
            model = pickle.load(file)

        z=model.predict([[First,Second,Third,Fourth]])
        params = {'pro':z}

    return render(request,'Pages/Machine_learning.html',params)


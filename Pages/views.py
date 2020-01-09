from django.shortcuts import render
from django.shortcuts import redirect
from .models import Dept, Hospital
from .filter import HospitalFilter
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn import metrics
import pandas as pd
import pickle
import calendar
import os
from datetime import date
import joblib
from django.conf import settings
import math
print("I have printed globally")
model = joblib.load('rf.pkl')
data = joblib.load('data.pkl')
once = 0
print("once = ",once)
def Documentation(request):
    print("Printed in ViewsDocumentation")
    global once 
    print(once)
    if once == 0 :
        column_name = ['Queue_number', 'Shift', 'date', 'Created_queue_hours',
                   'Waiting_duration', 'Number_of_wating_queue', 'Arrival_rate', 'Service_rate']
        data = pd.read_csv('http://bit.ly/deepblue_data',
                       header=0, names=column_name)
        dt = data['date'].str.split('/')
        dt2 = []
        for i in dt:
            i[0], i[1] = i[1], i[0]
            string = '/'
            i = string.join(i)
            dt2.append(i)
        data['date'] = pd.Series(dt2)
        data['date'] = pd.to_datetime(data['date'])
        data['weekdays'] = data['date'].dt.weekday
        data.drop('date', axis=1, inplace=True)
        y = data['Waiting_duration']
        X = data.drop('Waiting_duration', axis=1)
        # y = np.array(y)
        # X = np.array(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.30, random_state=42)
        rf = RandomForestRegressor(n_estimators=1000, random_state=42)
        rf.fit(X_train, y_train)
        prediction = rf.predict(X_test)
        error = abs(prediction - y_test)
        mape = 100*(error/y_test)
        accuracy = 100 - np.mean(mape)
        print('Accuracy:', round(accuracy, 2), '%.')
        path = os.path.join(settings.MODEL_ROOT, 'rf')
        with open(path, 'wb') as file:
            joblib.dump(rf, 'rf.pkl')
            joblib.dump(data, 'data.pkl')
        prediction_parameter = ([[101,   2,  14,  40,   4,   2,   6]])
        rf.predict(prediction_parameter)
        once = 1
    print(once)
    return render(request, 'Pages/Documentation.html')


def CompleteProcess(request, Hospital_id):
    print("Printed in CompleteProcess")
    x = Hospital.objects.get(Hospital_id=Hospital_id)
    params = {'HosId_id': x}

    if request.method == "POST":

        manual_prediction = []

        date = request.POST.get("Date")
        year, month, day = (int(i) for i in date.split('-'))
        weekday = calendar.weekday(year, month, day)

        time = request.POST.get('time')
        Hour, Mins = (int(i) for i in time.split(':'))
        if Mins > 30:
            Hour = Hour + 1
        created_queue_hour = int(Hour)

        count = int(request.POST.get('count'))

        for i in range(1, count+1):
            department = request.POST.get(str(i))
            manual_prediction.append(department)

        # path = os.path.join(settings.MODEL_ROOT, 'rf')
        # with open(path, 'rb') as file:
        #     model = joblib.load('rf.pkl')
        #     data = joblib.load('data.pkl')

        value = np.array([0])
        counter = 0
        for i in manual_prediction:

            queue_number = int(i)
            created_queue_hour = created_queue_hour + value[0]
            print(created_queue_hour)

            if created_queue_hour >= 18:
                break

            counter += 1

            if math.ceil(created_queue_hour) in [8, 9, 10, 11, 12]:
                shift = 1
            elif math.ceil(created_queue_hour) in [13, 14, 15, 16, 17, 18]:
                shift = 2
            else:
                shift = 3

            arrival_rate = data[(data['Created_queue_hours'] == math.ceil(created_queue_hour)) & (
                data['weekdays'] == weekday) & (data['Queue_number'] == queue_number)]['Arrival_rate'].max()
            service_rate = data[(data['Created_queue_hours'] == math.ceil(created_queue_hour)) & (
                data['weekdays'] == weekday) & (data['Queue_number'] == queue_number)]['Service_rate'].min()
            waiting_queue = data[(data['Created_queue_hours'] == math.ceil(created_queue_hour)) & (
                data['weekdays'] == weekday) & (data['Queue_number'] == queue_number)]['Number_of_wating_queue'].max()

            prediction_list = [queue_number, shift, created_queue_hour,
                               waiting_queue, arrival_rate, service_rate, weekday]
            prediction_parameter = np.array([prediction_list])
            value = value + model.predict(prediction_parameter)
        value = "{0:.2f}".format(round(value[0], 2))
        params = {'HosId_id': x, 'value': float(
            value), 'department': manual_prediction, 'count': count, 'counter': counter, 'diff': count-counter}
        print(value)

    return render(request, 'Pages/CompleteProcess1.html', params)


def Hospitals(request):
    print("Printed in Views.Hospitals")
    x = Hospital.objects.all()
    Hospital_filter = HospitalFilter(request.GET, queryset=x)
    # HospitalFilter(request.GET).data['Hospital_name'].upper()
    params = {'Pro': x, 'filter': Hospital_filter}
    if request.method == "POST":
        No = request.POST.get('Hospital_id')
        return redirect('http://localhost:8000/Hospital/'+No+'/Dashboard')
    return render(request, 'Pages/Hospitals.html', params)


def Dashboard(request, Hospital_id):
    print("Printed in Views.Dashboard")
    x = Hospital.objects.get(Hospital_id=Hospital_id)
    params = {'HosId_id': x}
    return render(request, 'Pages/Dashboard.html', params)


def Single(request, Hospital_id):
    print("Printed in Views.Single")
    a = Hospital.objects.get(Hospital_id=Hospital_id)
    x = Dept.objects.all()

    DepartmentList = []

    for i in x:
        DepartmentDict = {}
        DepartmentDict['Uid'] = str(i.Uid)
        DepartmentDict['Type'] = str(i.Type)
        DepartmentDict['Image'] = i.image
        DepartmentDict['Hospital_id'] = str(i.Hospital_id)
        DepartmentList.append(DepartmentDict)

    params = {'Pro': DepartmentList, 'HosId': Hospital_id, 'HosId_id': a}
    if request.method == "POST":
        No = request.POST.get('Dept_id')
        return redirect('/Hospital/'+Hospital_id+'/Dept/' + No)
    return render(request, 'Pages/Single.html', params)


def Complete(request, Hospital_id):

    x = Hospital.objects.get(Hospital_id=Hospital_id)
    params = {'HosId_id': x}

    print("Printed in Views.Complete")

    return render(request, 'Pages/Complete.html', params)


def Unknown(request, Hospital_id):
    print("Printed in Views.Unknown")
    a = Hospital.objects.get(Hospital_id=Hospital_id)
    x = Dept.objects.all()

    DepartmentList = []

    for i in x:
        DepartmentDict = {}
        DepartmentDict['Uid'] = str(i.Uid)
        DepartmentDict['Type'] = str(i.Type)
        DepartmentDict['Image'] = i.image
        DepartmentDict['Hospital_id'] = str(i.Hospital_id)
        DepartmentList.append(DepartmentDict)
    if request.method == "POST":
        No = request.POST.get('Dept_id')
        return redirect('/Hospital/' + Hospital_id + '/OurPredictions/' + No)

    params = {'Pro': DepartmentList, 'HosId': Hospital_id, 'HosId_id': a}
    return render(request, 'Pages/Unknown.html', params)


def Department(request, Hospital_id, UID):
    print("Printed in Views.Department")
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

    params = {'Pro': DepartmentList, 'Hos': HospitalList,
              'ProId': UID, 'HosId': Hospital_id, 'HosId_id': a}
    return render(request, 'Pages/Department.html', params)


# def Train(request):
#     print("Printed in Views.Train")
#     column_name = ['Queue_number', 'Shift', 'date', 'Created_queue_hours',
#                    'Waiting_duration', 'Number_of_wating_queue', 'Arrival_rate', 'Service_rate']
#     data = pd.read_csv('http://bit.ly/deepblue_data',
#                        header=0, names=column_name)
#     dt = data['date'].str.split('/')
#     dt2 = []
#     for i in dt:
#         i[0], i[1] = i[1], i[0]
#         string = '/'
#         i = string.join(i)
#         dt2.append(i)
#     data['date'] = pd.Series(dt2)
#     data['date'] = pd.to_datetime(data['date'])
#     data['weekdays'] = data['date'].dt.weekday
#     data.drop('date', axis=1, inplace=True)
#     y = data['Waiting_duration']
#     X = data.drop('Waiting_duration', axis=1)
#     # y = np.array(y)
#     # X = np.array(X)
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.30, random_state=42)
#     rf = RandomForestRegressor(n_estimators=1000, random_state=42)
#     rf.fit(X_train, y_train)
#     prediction = rf.predict(X_test)
#     error = abs(prediction - y_test)
#     mape = 100*(error/y_test)
#     accuracy = 100 - np.mean(mape)
#     print('Accuracy:', round(accuracy, 2), '%.')
#     path = os.path.join(settings.MODEL_ROOT, 'rf')
#     with open(path, 'wb') as file:
#         joblib.dump(rf, 'rf.pkl')
#         joblib.dump(data, 'data.pkl')
#     prediction_parameter = ([[101,   2,  14,  40,   4,   2,   6]])
#     rf.predict(prediction_parameter)

#     return render(request, 'Pages/sucess.html')


def Predict(request):

    z = None
    print("Printed in Views.Predict")
    params = {'pro': z}
    if request.method == "POST":
        Queue_number = request.POST.get('Queue_number')
        Queue_number = int(Queue_number)
        Date = request.POST.get('Date')
        year, month, day = (int(i) for i in Date.split('-'))
        dayNumber = calendar.weekday(year, month, day)
        days = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
        print(dayNumber, days[dayNumber])
        Time = request.POST.get('Time')
        Hour, Mins = (int(i) for i in Time.split(':'))
        if Mins > 30:
            Hour = Hour + 1
        Hour = int(Hour)
        print(Hour)
        print(Queue_number, type(Queue_number),
              Date, type(Date), Time, type(Time))
        # path = os.path.join(settings.MODEL_ROOT, 'rf')
        # with open(path, 'rb') as file:
        # model = joblib.load('rf.pkl')
        # data = joblib.load('data.pkl')
        print(type(data))
        print(data.head())
        shift = None
        if Hour in [8, 9, 10, 11, 12]:
            shift = 1
        elif Hour in [13, 14, 15, 16, 17, 18]:
            shift = 2
        else:
            shift = 3

        arrival_rate = data[(data['Created_queue_hours'] == Hour) & (
            data['weekdays'] == dayNumber)]['Arrival_rate'].max()
        service_rate = data[(data['Created_queue_hours'] == Hour) & (
            data['weekdays'] == dayNumber)]['Service_rate'].min()
        waiting_queue = data[(data['Created_queue_hours'] == Hour) & (
            data['weekdays'] == dayNumber)]['Number_of_wating_queue'].max()
        prediction_list = [Queue_number, shift, Hour,
                           waiting_queue, arrival_rate, service_rate, dayNumber]
        prediction_parameter = ([prediction_list])
        z = model.predict(prediction_parameter)[0]
        z = "{0:.2f}".format(round(z, 2))

        params = {'pro': z}

    return render(request, 'Pages/Machine_learning.html', params)


def OurPredictions(request, Hospital_id, UID):
    print("Printed in Views.OurPredictions")
    Date = str(date.today())
    year, month, day = (int(i) for i in Date.split('-'))
    dayNumber = calendar.weekday(year, month, day)
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    print(dayNumber, days[dayNumber])
    zlist = []
    # path = os.path.join(settings.MODEL_ROOT, 'rf')
    # with open(path, 'rb') as file:
    #     model = joblib.load('rf.pkl')
    #     data = joblib.load('data.pkl')

    for Hour in range(8, 18):
        shift = None
        if Hour in [8, 9, 10, 11, 12]:
            shift = 1
        elif Hour in [13, 14, 15, 16, 17, 18]:
            shift = 2
        else:
            shift = 3
        arrival_rate = data[(data['Created_queue_hours'] == Hour) & (
            data['weekdays'] == dayNumber)]['Arrival_rate'].max()
        service_rate = data[(data['Created_queue_hours'] == Hour) & (
            data['weekdays'] == dayNumber)]['Service_rate'].min()
        waiting_queue = data[(data['Created_queue_hours'] == Hour) & (
            data['weekdays'] == dayNumber)]['Number_of_wating_queue'].max()
        prediction_list = [UID, shift, Hour,
                           waiting_queue, arrival_rate, service_rate, dayNumber]
        prediction_parameter = ([prediction_list])
        z = model.predict(prediction_parameter)[0]
        z = "{0:.2f}".format(round(z, 2))
        zlist.append(z)
    params = {'Pro': UID, 'Day': days[dayNumber],
              'list': zlist, 'HosId_id': Hospital_id}
    return render(request, 'Pages/OurPredictions.html', params)

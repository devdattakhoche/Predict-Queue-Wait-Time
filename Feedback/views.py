import math
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import random 
import string
from django.views.decorators.csrf import csrf_exempt
import uuid
from .models import Feedback
from django.http import JsonResponse
import datetime
import csv
import os
import time
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@csrf_exempt
def generate(request):
    print("Printed in Views.generate")
    def ran_gen(size, chars=string.ascii_uppercase + string.digits): 
        return ''.join(random.choice(chars) for x in range(size))
    s=uuid.uuid4()
    s = str(s)
    today = date.today()
    # print(s)
    if request.method == 'POST':
        bks = Feedback(Uid=s[0:8], Date=today)
        bks.save()
        return JsonResponse({'s':s[0:8]})
    # fname = 'devdatta'.upper()
    # age = str(20)
    # param = fname + age
    # print(ran_gen(8,param))
    
    

    pro1 = {'pro':s[0:8]}
    return render(request,'Feedback/Token.html',pro1)

def feedback(request):
    if request.method == 'POST':
        Uid = request.POST.get('Uid')#Token
        Date = request.POST.get('Date')#Date
        Name = request.POST.get('Name')#Name
        DeptNo = request.POST.get('deptno')#department Number
        print("asdasdasdsada",DeptNo)
        Hour = request.POST.get('Hour')#Created_Queue_Hours
        Noqueue = request.POST.get('Noqueue')#No. of Queue
        Waiting = request.POST.get('Waiting')#Waiting duration
        Arrival = request.POST.get('Arrival')#Arrival Rate
        Service = request.POST.get('Service')#Service Rate
        print(Uid,Date,Name,Hour,Noqueue,Waiting,Arrival,Service)
  
        # print(Uid,"Uid","date:-",Date)
        try:
            obj=Feedback.objects.get(Uid=Uid)
        except ObjectDoesNotExist:
            obj = None
        if obj == None:
            print("I am in if")
            dict = {'pro':0}
            return render(request,'Feedback/index.html',dict)
        else:
            if Date!=obj.Date:
                print(Date,obj.Date)
                return render(request,'Feedback/index.html')
            else:
                x=list(Date.split("-"))
                x = x[2]+'/'+x[1]+'/'+x[0]
                print(x)
            if math.ceil(int(Hour)) in [8, 9, 10, 11, 12]:
                shift = 1
            elif math.ceil(int(Hour)) in [13, 14, 15, 16, 17, 18]:
                shift = 2
            else:
                shift = 3
            newrow = [DeptNo, shift, x, Hour, Waiting, Noqueue, Arrival, Service]
            path = os.path.join(BASE_DIR,'Pages\Train\data.csv')
            with open(path,'a',newline='') as outfile:
                append = csv.writer(outfile)
                append.writerow(newrow)
            print("I am in else")
            dict = {'pro':1}
            return render(request,'Feedback/index.html',dict)
    return render(request,'Feedback/index.html')

    

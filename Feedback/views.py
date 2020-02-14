import math
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render 
import random 
import string
from django.views.decorators.csrf import csrf_exempt
import uuid
from .models import Feed
from django.http import JsonResponse
import datetime
import csv
import os
import time
from datetime import date
from Pages.models import Hospital,Dept
flag = 0
token_generation = 0

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@csrf_exempt
def generate(request):
    global token_generation
    print("Printed in Views.generate")
    def ran_gen(size, chars=string.ascii_uppercase + string.digits): 
        return ''.join(random.choice(chars) for x in range(size))
    s=uuid.uuid4()
    s = str(s)
    today = date.today()
    Expiry = datetime.date.today() + datetime.timedelta(days=1)
    # print(s)
    if request.method == 'POST':
        token_generation = token_generation + 1
        bks = Feed(Uid=s[0:8], Date=today,Expiry=Expiry)
        bks.save()
        return JsonResponse({'s':s[0:8]})
    # fname = 'devdatta'.upper()
    # age = str(20)
    # param = fname + age
    # print(ran_gen(8,param))
    
    

    pro1 = {'pro':s[0:8]}
    return render(request,'Feedback/Token.html',pro1)
@csrf_exempt
def feedback(request):
    # Deparments = Dept.objects.filter(Hospital_id=slug)
    # params = {'dept':Departments}
    params = {}

    global flag
    if request.is_ajax():
        Uid = request.POST.get('Uid')#Token
        Date = request.POST.get('Date')
        try:
            x = Feed.objects.get(Uid=Uid)
        except ObjectDoesNotExist:
            x = None
        if x!=None:
            print("ajax called")
            return JsonResponse({'s':'1'})
        else :
            return JsonResponse({'s':'0'})
    if request.method == 'POST' and request.is_ajax() != True :
        Uid = request.POST.get('Uid')#Token
        Date = request.POST.get('Date')#Date
        Name = request.POST.get('Name')#Name
        DeptNo = request.POST.get('deptno')#department Number
        print("asdasdasdsada",DeptNo)
        Hour = request.POST.get('Hour')#Created_Queue_Hours
        Mins = request.POST.get('Mins')#Created_Queue_Hours
        Noqueue = request.POST.get('Noqueue')#No. of Queue
        Qhour = request.POST.get('Qhour')#Waiting duration
        Arrival = request.POST.get('Arrival')#Arrival Rate
        Service = request.POST.get('Service')#Service Rate
        print(Uid,Date,Name,Hour,Mins,Noqueue,Qhour,Arrival,Service)
  
        # print(Uid,"Uid","date:-",Date)
        try:
            queryset=Feed.objects.filter(Date=Date)
            obj=queryset.get(Uid=Uid)
            print(obj.Feedbacks)
            
        except ObjectDoesNotExist:
            obj = None
        if obj == None:
            print("I am in if")
            dict = {'pro':'wrong user'}
            return render(request,'Feedback/index.html',dict,params)
        else:
            if Date!=obj.Date:
                Feed.objects.filter(Expiry=Date).delete()
                print(Date,obj.Date)
                return render(request,'Feedback/index.html',params)
            else:
                x=list(Date.split("-"))
                x = x[2]+'/'+x[1]+'/'+x[0]
                y = Hour + "." + Mins
                print(y)
                print(x)
            if math.ceil(int(Hour)) in [8, 9, 10, 11, 12]:
                shift = 1
            elif math.ceil(int(Hour)) in [13, 14, 15, 16, 17, 18]:
                shift = 2
            else:
                shift = 3
            y=int(obj.Feedbacks) 
            print(y)
            y = y + 1
            # obj.save(Feedbacks=str(y))
            Feed.objects.filter(Uid=obj.Uid).update(Feedbacks=y)
            if obj.Feedbacks >= 5:
                obj.delete()
            print(obj.Expiry)
            newrow = [DeptNo, shift, x, Hour, y, Noqueue, Arrival, Service]
            path = os.path.join(BASE_DIR,'Pages\Train\data.csv')
            with open(path,'a',newline='') as outfile:
                append = csv.writer(outfile)
                append.writerow(newrow)
            print("I am in else")
            dict = {'pro':'You have successfully Submitted the feedback'}
            flag = flag + 1
            if flag == 100 :
                from Pages.Train import train
            if token_generation >=3:
                Feed.objects.filter(Expiry=Date).delete()
                    
            return render(request,'Feedback/succcess.html',dict,params)
    return render(request,'Feedback/index.html',params)

    

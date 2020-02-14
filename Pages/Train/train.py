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
# from django.conf import settings
import math 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR,'Train\data.csv')
print(path)
column_name = ['Queue_number', 'Shift', 'date', 'Created_queue_hours',
                   'Waiting_duration', 'Number_of_wating_queue', 'Arrival_rate', 'Service_rate']
data = pd.read_csv(path,
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
# path = os.path.join(settings.MODEL_ROOT, 'rf')
# with open(path, 'wb') as file:
#     joblib.dump(rf, 'rf.pkl')
#     joblib.dump(data, 'data.pkl')
prediction_parameter = ([[101,   2,  14,  40,   4,   2,   6]])
print(rf.predict(prediction_parameter))
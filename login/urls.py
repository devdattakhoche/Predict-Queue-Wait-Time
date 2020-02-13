from django.urls import path ,include
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('index/',views.index,name='index'),
    path('logout/',views.user_logout,name='logout'),
]


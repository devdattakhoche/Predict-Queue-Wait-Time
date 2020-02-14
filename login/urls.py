from django.urls import path ,include
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('index/',views.index,name='index'),
    path('logout/',views.user_logout,name='logout'),
    path('delele/',views.department_delete,name='delete'),
    path('update/',views.department_update,name='update'),
    path('update-form/<slug:slug>',views.update_form,name='update_form'),
    path('view/', views.view_department, name="view"),
]

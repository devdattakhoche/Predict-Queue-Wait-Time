from . import views
from django.urls import re_path, path

urlpatterns = [
 path('generate/', views.generate, name='generate'),
 path('feedback/',views.feedback,name = 'feedback'),
]

from . import views
from django.urls import re_path ,path


urlpatterns = [
    re_path(r'^Documentation/',views.Documentation,name='Documentation'),
    re_path(r'^Single/',views.Single,name='Single'),
    re_path(r'^Complete/',views.Complete,name='Complete'),
    re_path(r'^Unknown/',views.Unknown,name='Unknown'),
    path('Dept/Hid=<int:Hid>/Uid=<int:UID>',views.Department,name='Department'),
    re_path(r'^Hospitals/',views.Hospitals,name="Hospitals"),
    re_path(r'^Dashboard/(?:Huid-(?P<Hospital_id>\d+)/)?$',views.Dashboard,name="Dashboard"),
    # path("Single_hospital/<Hospital_id>",views.Single_hospital,name="Hospital")
    # path("Dept/<UID>",views.Department,name="Department")
    
]


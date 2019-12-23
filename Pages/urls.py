from . import views
from django.urls import re_path ,path


urlpatterns = [
    re_path(r'^Documentation/',views.Documentation,name='Documentation'),
    re_path(r'^Single/',views.Single,name='Single'),
    re_path(r'^Complete/',views.Complete,name='Complete'),
    re_path(r'^Unknown/',views.Unknown,name='Unknown'),
    re_path(r'^Dept/(?:UID=(?P<UID>\d+)/)?$',views.Department,name='Department'),
    path("Hospitals/",views.Hospitals,name="Hospitals"),
    path("Single_hospital/<Hospital_id>",views.Single_hospital,name="Hospital")
    # path("Dept/<UID>",views.Department,name="Department")
    
]


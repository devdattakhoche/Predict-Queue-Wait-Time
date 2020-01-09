from . import views
from django.urls import re_path, path

urlpatterns = [
    re_path(r'^Documentation/', views.Documentation, name='Documentation'),
    re_path(r'^Hospitals/', views.Hospitals, name="Hospitals"),
    path("Hospital/<Hospital_id>/Single", views.Single, name="Single"),
    path("Hospital/<Hospital_id>/Dashboard",views.Dashboard, name="Dashboard"),
    path("Hospital/<Hospital_id>/Complete", views.Complete, name="Complete"),
    path("Hospital/<Hospital_id>/Unknown", views.Unknown, name="Unknown"),
    path("Hospital/<Hospital_id>/Dept/<UID>", views.Department, name="Department"),
    path("Hospital/<Hospital_id>/OurPredictions/<UID>", views.OurPredictions, name="OurPredictions"),
    path("Predict", views.Predict, name="Predict"),
    # path("Train", views.Train, name="Train"),
    path("Hospital/<Hospital_id>/CompleteProcess1", views.CompleteProcess, name="CompleteProcess1"),

]

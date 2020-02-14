from django.contrib import admin
import os
from .models import Dept,Hospital
admin.site.register(Dept)
admin.site.register(Hospital)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from .models import Dept,Hospital,doctor
# admin.site.register(Dept)
# admin.site.register(Hospital)
admin.site.register(doctor)

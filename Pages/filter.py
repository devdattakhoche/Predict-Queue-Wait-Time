from .models import Hospital
import django_filters


class HospitalFilter(django_filters.FilterSet):
    class Meta:
        model = Hospital
        fields = ['Hospital_name']

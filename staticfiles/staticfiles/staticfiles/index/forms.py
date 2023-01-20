from django.forms import forms, ModelForm
from .models import Locations


class LocationsForm(ModelForm):

    class Meta:
        model = Locations
        fields = ("__all__")

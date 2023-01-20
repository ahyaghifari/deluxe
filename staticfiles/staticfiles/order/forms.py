from django.forms import ModelForm
from .models import Order


class OrderChangeStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
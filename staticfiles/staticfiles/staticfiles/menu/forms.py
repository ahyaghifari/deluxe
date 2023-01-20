from django import forms
from django.forms import ModelForm
from menu.models import Menu


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ['rating']

from django import forms
from django.forms import ModelForm
from .models import Contact, Subscribers


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ("__all__")


class SubscribersForm(ModelForm):

    class Meta:
        model = Subscribers
        fields = ("__all__")


class UnsubscribeForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'placeholder': "Email..."}))

    def clean_email(self):
        data = self.cleaned_data["email"]

        if not Subscribers.objects.filter(email=data).exists():
            raise forms.ValidationError("You are not subscribe", code="")
        elif Subscribers.objects.filter(email=data, active=False).exists():
            raise forms.ValidationError(
                "You already unsubscribe", code="")

        return data

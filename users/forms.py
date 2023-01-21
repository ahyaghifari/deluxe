from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserChangeForm
from users.models import User, UserToken


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', max_length=20, required=True)
    password = forms.CharField(
        label='Password', required=True, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    fullname = forms.CharField(label='Fullname', max_length=50, required=True)
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email', required=True)
    phone_number = forms.CharField(
        label='Phone Number', max_length=15, required=True)
    password1 = forms.CharField(
        label='Password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password', required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password not match", code="")

        return ValueError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password', 'last_login',
                   'is_superuser', 'first_name', 'last_name']


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label='Password', required=True, widget=forms.PasswordInput)
    newpassword = forms.CharField(
        label='New Password', required=True, widget=forms.PasswordInput)
    confirmnewpassword = forms.CharField(
        label='Confirm New Password', required=True, widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'placeholder': "Email..."}))

    def clean_email(self):
        data = self.cleaned_data["email"]

        if not User.objects.filter(email=data).exists():
            raise forms.ValidationError("Your email not in our data", code="")
        return data


class ResetPasswordForm(forms.Form):
    newpassword = forms.CharField(min_length=8, required=True, label="New Password",
                                  widget=forms.PasswordInput(attrs={'placeholder': "New password..."}))
    confirmnewpassword = forms.CharField(label="Confirm New Password", min_length=8, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': "Confirm new password..."}))

    def clean_confirmnewpassword(self):
        data = self.cleaned_data["confirmnewpassword"]
        newpassword = self.cleaned_data["newpassword"]

        if data != newpassword:
            raise forms.ValidationError("Your password not match")

        return data


class DeleteUserForm(forms.Form):
    username = forms.CharField(label="Your Username", required=True, widget=forms.TextInput(
        attrs={'placeholder': "Your username..."}))

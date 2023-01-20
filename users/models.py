from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(max_length=254, blank=False, unique=True)
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    expired_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user.username + " " + self.token


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_code = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    default = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.street + ", " + self.city + ", " + self.zip_code

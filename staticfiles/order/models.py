from django.db import models
from users.models import User
from menu.models import Menu


class Delivery(models.Model):
    cost = models.DecimalField(max_digits=10, decimal_places=2,  default=10000)


class Payment(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    type = models.CharField(max_length=50)
    channel_code = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=2500)

    def __str__(self):
        return self.name


class Status(models.Model):
    text = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    code = models.SmallIntegerField()

    def __str__(self):
        return self.text


class Order(models.Model):
    order_token = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.order_token


class OrderReceiver(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True)
    payment_token = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.payment_method


class OrderMenu(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.menu

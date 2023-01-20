from django.db import models

# Create your models here.


class Greeting(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Locations(models.Model):
    city = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.city


class About(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

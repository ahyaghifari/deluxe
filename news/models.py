from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    author = models.CharField(max_length=50)
    image = models.URLField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

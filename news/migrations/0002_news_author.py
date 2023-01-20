# Generated by Django 4.1.3 on 2022-12-28 06:54

from django.db import migrations, models
from news.seed import forwards_func, reverse_func


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="author",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_func, reverse_func)
    ]

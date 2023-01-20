# Generated by Django 4.1.3 on 2023-01-19 06:45

from django.db import migrations, transaction
from users.seed import forward_func, reverse_func
from django.contrib.auth.models import Group
from users.models import User


@transaction.atomic
def forwardcostumergroup(apps, schema_editor):
    Group.objects.create(name="Costumer")
    get = Group.objects.get(name="Costumer")
    users = User.objects.all()
    for user in users:
        user.groups.add(get)
        user.save()


@transaction.atomic
def reversecostumergroup(app, schema_editor):
    get = Group.objects.get(name="Costumer")
    users = User.objects.all()
    for user in users:
        user.groups.remove(get)
        user.save()

    users.delete()
    get.delete()


@transaction.atomic
def forwardordermanagergroup(app, schema_editor):
    Group.objects.create(name="OrderManager")


@transaction.atomic
def reverseordermanagergroup(app, schema_editor):
    get = Group.objects.get(name="OrderManager")
    get.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func),
        migrations.RunPython(forwardcostumergroup, reversecostumergroup),
        migrations.RunPython(forwardordermanagergroup,
                             reverseordermanagergroup),
    ]

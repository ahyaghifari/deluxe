from django.core.management import call_command


def forwards_func(apps, schema_editor):
    call_command('loaddata', 'category.json')
    call_command('loaddata', 'menu.json')
    call_command('loaddata', 'rate.json')
    call_command('loaddata', 'comment.json')


def reverse_func(apps, schema_editor):
    Comment = apps.get_model('menu', 'Comment')
    Comment.objects.all().delete()
    Rate = apps.get_model('menu', 'Rate')
    Rate.objects.all().delete()
    Menu = apps.get_model('menu', 'Menu')
    Menu.objects.all().delete()
    Category = apps.get_model('menu', 'Category')
    Category.objects.all().delete()

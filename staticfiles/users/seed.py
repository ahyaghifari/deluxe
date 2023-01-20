from django.core.management import call_command

def forward_func(apps, schema_editor):
    call_command('loaddata', 'users.json')


def reverse_func(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.all().delete()

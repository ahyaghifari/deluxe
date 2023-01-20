
from django.db import migrations
from menu.seed import forwards_func, reverse_func
from menu.models import Menu, Rate


def forward(apps, schema_editor):

    menu = Menu.objects.all()

    for m in menu:
        star5 = Rate.objects.filter(menu=m, rating=5).count()
        star4 = Rate.objects.filter(menu=m, rating=4).count()
        star3 = Rate.objects.filter(menu=m, rating=3).count()
        star2 = Rate.objects.filter(menu=m, rating=2).count()
        star1 = Rate.objects.filter(menu=m, rating=1).count()

        score = star5 * 5 + star4 * 4 + star3 * 3 + star2 * 2 + star1 * 1
        responses = star5 + star4 + star3 + star2 + star1

        scoretotal = score / responses

        m.rating = scoretotal
        m.save()


def rev(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0002_menu_active_menu_rating_alter_menu_category_rate_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RunPython(forward, rev)
    ]

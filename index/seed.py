def forwards_func(apps, schema_editor):

    Greeting = apps.get_model('index', 'Greeting')
    g1 = Greeting(
        text="happy to see you today, i hope to see you again tomorrow and future. So we can meet again and share happines for this life :)")
    g1.save()

    Locations = apps.get_model('index', 'Locations')
    l1 = Locations(city="Banjarmasin", address="Jl. A. Yani Km.15 No. 30",
                   image="https://www.indonesia.travel/content/dam/indtravelrevamp/en/news-events/news/7-amazing-places-you-need-to-visit-in-banjarmasin/7bf161fbd6679451acd35770cdccbd9d21146a71-92dea.jpg")
    l2 = Locations(city="Martapura", address="Jl. A. Yani Km.37 No. 21",
                   image="https://asset.kompas.com/crops/C5JBQuEXKO5QhEMn9hgM3yhZqN4=/2x0:1000x665/750x500/data/photo/2022/04/02/6247f6cb8d265.jpg")
    l3 = Locations(city="Makassar", address="Jl. Jenderal Soedirman No. 10",
                   image="https://akcdn.detik.net.id/community/pasma/2017/01/08/14838521291109836137.jpg?w=942")

    lall = [l1, l2, l3]
    for l in lall:
        l.save()

    About = apps.get_model('index', 'About')
    a1 = About(
        text="Deluxe is next project by ahyaghifari, in the middle of 2022, i make project website gfk-food and that about food e-commerce by gfk-food using Laravel. But the project has stop anyway. So i decide to remake the project with Django now, hope you like it. <br><br> Deluxe or gfk-food is about one food store sell pastry, and more like ice cream, donut, and dessert.")
    a1.save()


def reverse_func(apps, schema_editor):
    Greeting = apps.get_model('index', 'Greeting')
    Greeting.objects.all().delete()
    Locations = apps.get_model('index', 'Locations')
    Locations.objects.all().delete()
    About = apps.get_model('index', 'About')
    About.objects.all().delete()

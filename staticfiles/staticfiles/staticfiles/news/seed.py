def forwards_func(apps, schema_editor):
    News = apps.get_model('news', 'News')
    n1 = News(title="New Menu Choco Volcano", slug="new-menu-choco-volcano", author="ahyaghifari",
              image="https://food-images.files.bbci.co.uk/food/recipes/chocolate_volcanoes_37330_16x9.jpg", body="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Deleniti temporibus corporis minus libero repudiandae aut illo expedita! Ut nobis mollitia veritatis nihil aliquam delectus sunt explicabo necessitatibus animi, in velit deserunt iure soluta rem dolore. Nostrum delectus dolore voluptates recusandae ducimus maxime molestias animi reprehenderit, id maiores. Amet quam obcaecati labore corporis repellat cum dolore, vero impedit laudantium suscipit, animi ullam! Necessitatibus, odio sunt dolorem labore animi, nesciunt nam nihil cumque vitae odit praesentium, corrupti rem commodi eaque ducimus tempore itaque perspiciatis quos facere nulla cupiditate libero voluptate veniam? Cum in nulla cupiditate fuga! Praesentium ipsum minus fuga dolore a.")
    n2 = News(title="Event Happy New Year", slug="event-happy-new-year", author="ahyaghifari",
              image="https://c.tadst.com/gfx/750w/fireworks-in-the-sky.jpg", body="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Deleniti temporibus corporis minus libero repudiandae aut illo expedita! Ut nobis mollitia veritatis nihil aliquam delectus sunt explicabo necessitatibus animi, in velit deserunt iure soluta rem dolore. Nostrum delectus dolore voluptates recusandae ducimus maxime molestias animi reprehenderit, id maiores. Amet quam obcaecati labore corporis repellat cum dolore, vero impedit laudantium suscipit, animi ullam! Necessitatibus, odio sunt dolorem labore animi, nesciunt nam nihil cumque vitae odit praesentium, corrupti rem commodi eaque ducimus tempore itaque perspiciatis quos facere nulla cupiditate libero voluptate veniam? Cum in nulla cupiditate fuga! Praesentium ipsum minus fuga dolore a.")
    n3 = News(title="New Interior Set", slug="new-interior-set", author="ahyaghifari",
              image="https://www.saunamanufacture.com/cch/bakery-and-cafe-design-d79360.jpg", body="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Deleniti temporibus corporis minus libero repudiandae aut illo expedita! Ut nobis mollitia veritatis nihil aliquam delectus sunt explicabo necessitatibus animi, in velit deserunt iure soluta rem dolore. Nostrum delectus dolore voluptates recusandae ducimus maxime molestias animi reprehenderit, id maiores. Amet quam obcaecati labore corporis repellat cum dolore, vero impedit laudantium suscipit, animi ullam! Necessitatibus, odio sunt dolorem labore animi, nesciunt nam nihil cumque vitae odit praesentium, corrupti rem commodi eaque ducimus tempore itaque perspiciatis quos facere nulla cupiditate libero voluptate veniam? Cum in nulla cupiditate fuga! Praesentium ipsum minus fuga dolore a.")

    nall = [n1, n2, n3]

    for n in nall:
        n.save()


def reverse_func(apps, schema_editor):
    News = apps.get_model('nrsews', 'News')
    News.objects.all().delete()

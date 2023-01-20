def forwards_func(apps, schema_editor):
    Delivery = apps.get_model('order', 'Delivery')
    Delivery(cost=10000).save()

    Payment = apps.get_model('order', 'Payment')
    p1 = Payment(name="COD", slug="cod", type="cod",
                 channel_code="COD", fee=2500)
    p2 = Payment(name="Indomaret", slug="indomaret",
                 type="retail-outlet", channel_code="INDOMARET", fee=2500)
    p3 = Payment(name="Alfamart", slug="alfamart",
                 type="retail-outlet", channel_code="ALFAMART", fee=2500)
    pall = [p1, p2, p3]
    for p in pall:
        p.save()

    Status = apps.get_model('order', 'Status')
    s1 = Status(text='Not Paid', status='notpaid', code=101)
    s2 = Status(text='On Process', status='onprocess', code=101)
    s3 = Status(text='On The Way', status='ontheway', code=101)
    s4 = Status(text='Received', status='received', code=202)
    s5 = Status(text='Finished', status='finished', code=303)
    s6 = Status(text='Canceled', status='canceled', code=404)

    sall = [s1, s2, s3, s4, s5, s6]
    for s in sall:
        s.save()


def reverse_func(apps, schema_editor):
    Status = apps.get_model('order', 'Status')
    Status.objects.all().delete()
    Payment = apps.get_model('order', 'Payment')
    Payment.objects.all().delete()
    Delivery = apps.get_model('order', 'Delivery')
    Delivery.objects.all().delete()

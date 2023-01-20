from django import template

register = template.Library()


@register.filter
def statustext(status):
    if status == "notpaid":
        return "bg-neutral-800"
    elif status == "onprocess":
        return "bg-brown"
    elif status == "ontheway":
        return "bg-sky-700"
    elif status == "received":
        return "bg-teal-700"
    elif status == "finished":
        return "bg-green-700"
    elif status == "canceled":
        return "bg-red-700"
    return status


@register.filter
def myrange(value):
    if value == 0 or value == None:
        return []
    return range(value)


@register.filter
def myint(value):
    return int(value)


@register.filter
def changezero(value):
    return 0


@register.filter
def ordermanagergate(user):
    return user.groups.filter(name="OrderManager").exists()


@register.filter
def customergate(user):
    return user.groups.filter(name="Costumer").exists()

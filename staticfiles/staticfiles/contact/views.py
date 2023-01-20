from django.shortcuts import render, redirect
from .forms import ContactForm, SubscribersForm, UnsubscribeForm
from django.http import HttpResponseNotFound, JsonResponse
from .models import Contact, Subscribers
from manager.filters import ContactFilter
from deluxe.decorators import superuser_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    context = {
        'title': 'Contact',
        'form': ContactForm
    }
    return render(request, 'contact.html', context)


@staff_member_required
def contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    filter = ContactFilter(request.GET, queryset=contacts)
    contacts = filter.qs

    context = {
        'title': "Contacts",
        'contacts': contacts,
        'contactsfilter' : filter,
        'context' : "all"
    }
    return render(request, 'contacts.html', context)

def contactdetail(request, pk):
    contact = Contact.objects.get(pk=pk)

    context = {
        'title' : "Contact Detail",
        'contact' : contact,
        'context' : 'detail'
    }
    return render(request, 'contacts.html', context)


def create(request):
    if request.method == "POST":
        formset = ContactForm(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Thank you for your message")
            return redirect('/contact/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


def subscribe(request):
    if request.method == "POST":
        confirm = ""
        message = ""
        email = request.POST['email']

        if Subscribers.objects.filter(email=email, active=True).exists():
            confirm = "400"
            message = f"Your email {email} is already registered"

        if Subscribers.objects.filter(email=email, active=False).exists():
            getsubscriber = Subscribers.objects.filter(email=email).get()
            getsubscriber.active = True
            getsubscriber.save()
            confirm = "200"
            message = f"Your email {email} is subscribe again"

        if not Subscribers.objects.filter(email=email).exists():
            createsubscriber = Subscribers(email=email, active=True)
            createsubscriber.save()
            confirm = "200"
            message = f"Your email success subscribe, check your email {email}"

        return JsonResponse({
            'confirm':  confirm,
            'message': message,
            'email': email
        })
    return HttpResponseNotFound(render(request, 'pages/404.html'))


def unsubscribe(request):
    form = UnsubscribeForm

    if request.method == "POST":
        form = UnsubscribeForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            getsubscriber = Subscribers.objects.get(email=email)
            getsubscriber.active = False
            getsubscriber.save()

            messages.success(request, "You just Unsubscribe")
            return redirect('/contact/')
        return render(request, 'unsubscribe.html', {'title': "Unsubscribe", 'form': form})

    return render(request, 'unsubscribe.html', {'title': "Unsubscribe", 'form': form})


@superuser_required
def updatesubscriber(request):
    if request.method == "POST":
        oldemail = request.POST['oldemail']
        getemail = Subscribers.objects.filter(email=oldemail).get()
        formset = SubscribersForm(request.POST, instance=getemail)
        if formset.is_valid():
            formset.save()
            return redirect('/manager/subscribers/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@superuser_required
def deletesubscriber(request):
    if request.method == "POST":
        email = request.POST['email']
        subscriber = Subscribers.objects.filter(email=email).get()
        subscriber.delete()
        return redirect('/manager/subscribers/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))

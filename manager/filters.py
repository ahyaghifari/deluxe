import django_filters
from django_filters import CharFilter, OrderingFilter
from menu.models import Menu
from cart.models import Cart
from news.models import News
from order.models import Order
from users.models import User
from contact.models import Contact, Subscribers


class MenuFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label="Name")
    sort = OrderingFilter(
        fields=('price', 'rating', 'created_at'), label="Sort By")

    class Meta:
        model = Menu
        fields = ['category']


class NewsFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains', label="Title")
    author = CharFilter(field_name='author',
                        lookup_expr='icontains', label='Author')
    sort = OrderingFilter(fields=('created_at', 'created_at'), label="Sort By")

    class Meta:
        model = News
        fields = []


class CartFilter(django_filters.FilterSet):
    user = CharFilter(field_name='user__username',
                      lookup_expr='icontains', label="Username")
    sort = OrderingFilter(fields=('total', 'total'), label="Total")

    class Meta:
        model = Cart
        fields = []


class OrderFilter(django_filters.FilterSet):
    user = CharFilter(field_name='user__username',
                      lookup_expr='icontains', label="Username")
    sort = OrderingFilter(
        fields=('total', 'created_at'), label="Sort By")

    class Meta:
        model = Order
        fields = ['status']


class OrderManagerFilter(django_filters.FilterSet):
    user = CharFilter(field_name='user__username',
                      lookup_expr='icontains', label="User")
    sort = OrderingFilter(fields=(('total', 'total'), (
        'created_at', 'created_at'
    )), label="Sort By")
    # created = OrderingFilter(fields=('created_at'), label="Created")

    class Meta:
        model = Order
        fields = ['status']


class UserFilter(django_filters.FilterSet):
    name = CharFilter(field_name='username',
                      lookup_expr='icontains', label="Username")

    class Meta:
        model = User
        fields = ['groups', 'is_staff']


class ContactFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains', label="Name")
    email = CharFilter(field_name='email',
                       lookup_expr='icontains', label="Email")
    sort = OrderingFilter(fields=('created_at', 'created_at'), label="Sort By")

    class Meta:
        model = Contact
        fields = []


class SubscribersFilter(django_filters.FilterSet):
    email = CharFilter(field_name='email',
                       lookup_expr='icontains', label="Email")
    sort = OrderingFilter(fields=('created_at', 'created_at'), label="Sort By")

    class Meta:
        model = Subscribers
        fields = ['active']

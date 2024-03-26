from django import template
#from orders.views import Order, OrderDetails
from orders.models import Order, OrderDetails
from accounts.models import Store
from products.models import Product 
from django.contrib.auth.models import User
from django.utils import timezone

register = template.Library()

@register.filter
def all_orders_count(user):
    if user.is_authenticated and not user.is_anonymous:
        if Order.objects.all():
            all_order = Order.objects.all().count()
            return all_order

        else:
            return 0



@register.filter
def all_orders_revenue(user):
    if user.is_authenticated and not user.is_anonymous:
        orders = Order.objects.all()  # Assuming there's a 'user' field in your Order model

        # Convert non-empty amounts to float and calculate total revenue
        total_revenue = sum(float(order.amount) if order.amount else 0 for order in orders)
        return total_revenue
    else:
        return 0

@register.filter
def all_store_count(user):
    if user.is_authenticated and not user.is_anonymous:
        if Store.objects.all():
            all_count = Store.objects.all().count()
            return all_count

        else:
            return 0



@register.filter
def all_products_count(user):
    if user.is_authenticated and not user.is_anonymous:
        if Product.objects.all():
            all_products = Product.objects.all().count()
            return all_products

        else:
            return 0
        


@register.filter
def all_users_count(user):
    if user.is_authenticated and not user.is_anonymous:
        if User.objects.all():
            all_users = User.objects.all().count()
            return all_users

        else:
            return 0
        

@register.filter
def cart_items_count(user):
    if user.is_authenticated and not user.is_anonymous:
        if Order.objects.all().filter(user=user, is_finished=False):
            order = Order.objects.get(user=user, is_finished=False)
            return OrderDetails.objects.all().filter(order=order).count()

        else:
            return 0



@register.filter
def underway_orders_count(user):
    if user.is_authenticated and not user.is_anonymous:
        if Order.objects.all().filter(status="Underway"):
            underway_orders = Order.objects.all().filter(status="Underway").count()
            return underway_orders

        else:
            return 0

from django.contrib import admin
from .models import Profile,BankAccount ,SocialLink, Store
from orders.models import Order
from products.models import Product
# Register your models here.

from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import User

from django.contrib.admin import SimpleListFilter
from datetime import datetime

# Use filter later 
# class TotalSpendFilter(SimpleListFilter):
#     title = 'Total Spend Range'
#     parameter_name = 'total_spend'

#     def lookups(self, request, model_admin):
#         return (
#             ('low', 'Low'),
#             ('medium', 'Medium'),
#             ('high', 'High'),
#         )

#     def queryset(self, request, queryset):
#         if self.value() == 'low':
#             return queryset.filter(total_spend__lte=100)
#         elif self.value() == 'medium':
#             return queryset.filter(total_spend__range=(101, 500))
#         elif self.value() == 'high':
#             return queryset.filter(total_spend__gt=500)

class RegistrationDateFilter(SimpleListFilter):
    title = 'Registration Date Range'
    parameter_name = 'registration_date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
            ('this_year', 'This Year'),
        )

    def queryset(self, request, queryset):
        from datetime import date, timedelta

        if self.value() == 'today':
            return queryset.filter(date=date.today())
        elif self.value() == 'this_week':
            start_date = date.today() - timedelta(days=date.today().weekday())
            return queryset.filter(date__range=[start_date, date.today()])
        elif self.value() == 'this_month':
            return queryset.filter(date__month=date.today().month, date__year=date.today().year)
        elif self.value() == 'this_year':
            return queryset.filter(date__year=date.today().year)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'email', 'address', 'created_date', 'order_count', 'type','status','custom_actions',)
    # list_filter = ("type",)
    list_display_links = None
    list_per_page = 10
    search_fields = ('user__username',)
    list_filter = (
        'user__is_active',
        'address',  # Replace 'location' with the actual field name
        RegistrationDateFilter,
        # TotalSpendFilter,
    )

    def created_date(self, obj):
        date_object = obj.date
        formatted_date = date_object.strftime('%d-%m-%Y')
        return formatted_date

    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_authenticated:
            queryset = queryset.exclude(user=request.user)
            # queryset = queryset.exclude(type='vendor')
        return queryset

    def custom_actions(self, obj):
        edit_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        status_button = 'Disable' if obj.user.is_active else 'Enable'
        status_action_url = reverse('accounts:toggle_status', args=[obj.pk])

        if obj.user.is_active:
            # Include confirmation script for disabling
            return format_html(
                '<a class="p-1 bg-success" href="{}" style="border-radius:0.25rem;">View</a>&nbsp;&nbsp;'
                '<a class="p-1 bg-info" href="{}" style="border-radius:0.25rem;" onclick="return confirmStatusChange(\'{}\', \'{}\', \'{}\');">{}</a>',
                edit_url, status_action_url, status_action_url, obj.user.username, status_button, status_button,
            )
        else:
            # No confirmation script for enabling
            return format_html(
                '<a class="p-1 bg-success" href="{}" style="border-radius:0.25rem;">View</a>&nbsp;&nbsp;'
                '<a class="p-1 bg-info" href="{}" style="border-radius:0.25rem;">{}</a>',
                edit_url, status_action_url, status_button,
            )

    custom_actions.short_description = 'Actions'

    def order_count(self, obj):
        return Order.objects.filter(user=obj.user).count()

    order_count.short_description = 'No. Orders'

    def status(self,obj):
        if obj.user.is_active:
            return "Active"
        else :
            return "Blocked"

class BankAccountAdmin(admin.ModelAdmin):
    # inlines = [Inline_ProductImage, Inline_ProductAlternative]
    fields = ("vendor_profile","bank_name", "account_number",  "swift_code",
              "account_name", "country","paypal_email","description",)
    list_display = ("id", "vendor_profile", "bank_name","account_number",
                    "swift_code", "account_name","country","paypal_email",)
    list_display_links = ("id", "bank_name", "paypal_email")

    search_fields = ("account_name", )
    list_per_page = 10

class SocialLinkAdmin(admin.ModelAdmin):
    # inlines = [Inline_ProductImage, Inline_ProductAlternative]
    fields = ("vendor_profile","facebook", "twitter",  "instagram",
              "pinterest",)
    list_display = ("id", "vendor_profile", "facebook","twitter",
                    "instagram", "pinterest",)
    list_display_links = ("id", "vendor_profile", )
    

    search_fields = ("id", )
    list_per_page = 10    


class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'owner_name', 'email', 'contact_number','date_created', 'product_count', 'status', 'custom_actions')
    search_fields = ('store_name', 'owner_name', 'email', 'business_registration_number')
    list_filter = ('store_type',)
    ordering = ('store_name',)
    list_display_links = ("store_name",)
    list_per_page = 10

    def product_count(self, obj):
        return Product.objects.filter(product_vendor=obj.owner_name).count()
    
    def status(self, obj):
        vendor_obj = Profile.objects.get(user__username=obj.owner_name)
        if vendor_obj.admission:
            return "Verified"
        else :
            return "Pending"

    def custom_actions(self, obj):
        edit_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])

        return format_html(
            '<a class="p-1 bg-success" href="{}" style="border-radius:0.25rem;">View</a>&nbsp;&nbsp;'
            '<a class="p-1 bg-danger" href="{}" style="border-radius:0.25rem;">Delete</a>',
            edit_url, delete_url, 
        )
    def changelist_view(self, request, extra_context=None):
        # Calculate the total count of your model
        total_count = self.model.objects.count()

        # Add the total count to the extra_context
        extra_context = extra_context or {}
        extra_context['count_flag'] = True
        extra_context['total_count'] = total_count

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Profile,ProfileAdmin)
admin.site.register(BankAccount,BankAccountAdmin)
admin.site.register(SocialLink,SocialLinkAdmin)
admin.site.register(Store, StoreAdmin )
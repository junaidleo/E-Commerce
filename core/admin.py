from django.contrib import admin

from .models import Item, OrderItem, Order, Address

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address'
                    ]
    list_display_links = [
        'user',
        'shipping_address'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received']
    search_fields = [
        'user__username',
        'ref_code'
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone_number',
        'street_address',
        'apartment_address',
        'state',
        'zip',
        'default'
    ]
    list_filter = ['default','state']
    search_fields = ['user','phone_number', 'street_address', 'apartment_address','state', 'zip']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
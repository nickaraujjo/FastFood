from django.contrib import admin
from .models import DeliveryPerson, Delivery


@admin.register(DeliveryPerson)
class DeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'vehicle', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'phone']
    list_editable = ['status']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'delivery_person', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order__id', 'delivery_person__name']
    readonly_fields = ['created_at', 'updated_at']

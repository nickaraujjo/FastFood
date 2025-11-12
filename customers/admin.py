from django.contrib import admin
from .models import Customer, Referral


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'loyalty_points', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred', 'bonus_points', 'created_at']
    search_fields = ['referrer__name', 'referred__name']
    readonly_fields = ['created_at']

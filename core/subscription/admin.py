from django.contrib import admin

from subscription.models import Subscription, Payment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "uid",
        "type",
        "user",
        "active_until",
        "is_active",
        "created",
        "updated",
    ]
    list_filter = [
        "type",
        "updated",
    ]
    date_hierarchy = "updated"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "uid",
        "state",
        "provider",
        "amount",
        "currency",
        "user",
        "created",
        "updated",
    ]
    list_filter = [
        "state",
        "provider",
        "created",
    ]
    date_hierarchy = "created"

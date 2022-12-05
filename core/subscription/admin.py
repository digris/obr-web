from django.contrib import admin

from subscription.models import Payment, Redemption, Subscription, Voucher


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
    search_fields = [
        "uid",
        "user__email",
        "user__uid",
    ]
    list_filter = [
        "type",
        "updated",
    ]
    readonly_fields = [
        "user",
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


class RedemptionInline(admin.TabularInline):
    model = Redemption

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = [
        "user",
        "created",
    ]


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "uid",
        "code_display",
        "user",
        "num_days",
        "num_used",
        "is_valid_display",
    ]
    search_fields = [
        "uid",
        "code",
        "user__uid",
        "user__email",
    ]
    raw_id_fields = [
        "user",
    ]
    date_hierarchy = "created"

    inlines = [
        RedemptionInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [
                "code",
            ]
        return []

    @admin.display(
        boolean=True,
        description="Valid",
    )
    def is_valid_display(self, obj):
        return obj.is_valid


@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "uid",
        "voucher",
        "user",
        "created",
    ]
    search_fields = [
        "voucher__code",
        "voucher__uid",
        "user__email",
        "user__uid",
    ]
    date_hierarchy = "created"
    raw_id_fields = [
        "voucher",
        "user",
    ]

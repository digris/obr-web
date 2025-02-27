from django.contrib import admin

import unfold.admin
import unfold.decorators
from subscription.models import (
    Payment,
    PaymentState,
    Redemption,
    Subscription,
    SubscriptionType,
    Voucher,
)


@admin.register(Subscription)
class SubscriptionAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True

    date_hierarchy = "updated"
    list_display = [
        "user",
        "is_active_display",
        "type_display",
        "active_until",
        "created",
        "updated",
        "uid_display",
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

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="type",
        ordering="type",
        label={
            SubscriptionType.PLAN: "success",
            SubscriptionType.TRIAL: "info",
        },
    )
    def type_display(self, obj):
        return obj.type

    @unfold.decorators.display(
        description="active",
        ordering="is_active",
        label={
            "active": "success",
            "inactive": "-",
        },
    )
    def is_active_display(self, obj):
        return "active" if obj.is_active else "inactive"

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid


@admin.register(Payment)
class PaymentAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True

    date_hierarchy = "created"
    list_display = [
        "user",
        "state_display",
        "amount",
        "currency",
        "provider",
        "created",
        "updated",
        "uid_display",
    ]
    list_filter = [
        "state",
        "provider",
        "created",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="state",
        ordering="state",
        label={
            PaymentState.PAID: "success",
            PaymentState.INITIALIZED: "info",
            PaymentState.PENDING: "warning",
        },
    )
    def state_display(self, obj):
        return obj.state

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid


class RedemptionInline(unfold.admin.TabularInline):
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
class VoucherAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = False

    date_hierarchy = "created"
    list_display = [
        "user",
        "is_valid_display",
        "code_display",
        "num_used",
        "num_days",
        "valid_until",
        "inherit_display",
        "parent",
        "uid_display",
    ]
    search_fields = [
        "uid",
        "code",
        "user__uid",
        "user__email",
    ]
    raw_id_fields = [
        "parent",
        "user",
    ]

    inlines = [
        RedemptionInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [
                "code",
            ]
        return []

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="code",
        label=True,
    )
    def code_display(self, obj):
        return obj.code_display

    @unfold.decorators.display(
        description="valid",
        label={
            "valid": "success",
            "expired": "warning",
        },
    )
    def is_valid_display(self, obj):
        return "valid" if obj.is_valid else "expired"

    @unfold.decorators.display(
        description="inherit",
        label={
            "yes": "info",
        },
    )
    def inherit_display(self, obj):
        return "yes" if obj.inherit else "no"

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid


@admin.register(Redemption)
class RedemptionAdmin(unfold.admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "user",
        "code_display",
        "created",
        "uid_display",
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

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="code",
        label=True,
    )
    def code_display(self, obj):
        return obj.voucher

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid

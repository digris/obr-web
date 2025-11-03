from django.contrib import admin

import unfold.admin
import unfold.decorators
from donation.models import Donation
from unfold.contrib.filters.admin import RangeDateFilter


@admin.register(Donation)
class DonationAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True

    date_hierarchy = "created"
    list_display = [
        "state_display",
        "kind_display",
        "client_mode_display",
        "user_display",
        "amount",
        "currency",
        "created",
        "uid_display",
    ]
    search_fields = [
        "uid",
        "user__email",
        "user__uid",
    ]
    list_filter = [
        "kind",
        "state",
        ("updated", RangeDateFilter),
    ]
    readonly_fields = [
        "user",
        "user_identity",
        "kind",
        "client_mode",
        "state",
        "amount",
        "currency",
        "payment_intent_id",
        "price_id",
        "subscription_id",
        "payment_intent_data",
        "subscription_data",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="user",
    )
    def user_display(self, obj):
        return str(obj.user) if obj.user else "Anonymous User"

    @unfold.decorators.display(
        description="kind",
        ordering="kind",
        label={
            Donation.Kind.SINGLE: "",
            Donation.Kind.RECURRING: "",
        },
    )
    def kind_display(self, obj):
        return obj.kind, obj.get_kind_display()

    @unfold.decorators.display(
        description="client",
        ordering="client_mode",
        label=True,
    )
    def client_mode_display(self, obj):
        return obj.get_client_mode_display()

    @unfold.decorators.display(
        description="state",
        ordering="state",
        label={
            Donation.State.PENDING: "info",
            Donation.State.FAILED: "danger",
            Donation.State.SUCCEEDED: "success",
            Donation.State.ACTIVE: "success",
            Donation.State.CANCELED: "warning",
            Donation.State.EXPIRED: "warning",
        },
    )
    def state_display(self, obj):
        return obj.state, obj.get_state_display()

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid

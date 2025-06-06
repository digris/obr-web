from django.contrib import admin

import unfold.admin
import unfold.decorators
from donation.models import RecurringDonation, SingleDonation


@admin.register(SingleDonation)
class SingleDonationAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True

    date_hierarchy = "updated"
    list_display = [
        "user_display",
        "state_display",
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
        "state",
        "updated",
    ]
    readonly_fields = [
        "user",
        "user_identity",
        "state",
        "amount",
        "currency",
        "payment_intent_id",
        "extra_data",
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
        description="state",
        ordering="state",
        label={
            SingleDonation.State.PENDING: "info",
            SingleDonation.State.SUCCEEDED: "success",
            SingleDonation.State.FAILED: "danger",
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


@admin.register(RecurringDonation)
class RecurringDonationAdmin(unfold.admin.ModelAdmin):
    compressed_fields = True

    date_hierarchy = "updated"
    list_display = [
        "user_display",
        "state_display",
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
        "state",
        "updated",
    ]
    readonly_fields = [
        "user",
        "state",
        "amount",
        "currency",
        "payment_intent_id",
        "subscription_id",
        "extra_data",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="user",
    )
    def user_display(self, obj):
        return str(obj.user)

    @unfold.decorators.display(
        description="state",
        ordering="state",
        label={
            RecurringDonation.State.PENDING: "info",
            RecurringDonation.State.ACTIVE: "success",
            RecurringDonation.State.CANCELED: "warning",
            RecurringDonation.State.EXPIRED: "warning",
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

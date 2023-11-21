from rest_framework.permissions import BasePermission

# see account `GlobalPermissions`
VIEW_PERMISSION = "account.api_stats_view"
WEBHOOK_PERMISSION = "account.api_stats_webhooks"
EVENT_CREATE_PERMISSION = "account.api_stats_event_create"


class ViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(VIEW_PERMISSION)


class WebhookPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(WEBHOOK_PERMISSION)


class EventCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(EVENT_CREATE_PERMISSION)

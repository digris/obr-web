from rest_framework.permissions import BasePermission


# see account `GlobalPermissions`
SYNC_PERMISSION = "account.api_sync_webhooks"


class SyncAPIPermission(BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return request.user.has_perm(SYNC_PERMISSION)

from rest_framework.permissions import BasePermission

# see account `GlobalPermissions`
STATS_PERMISSION = "account.api_stats_webhooks"


class StatsAPIPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(STATS_PERMISSION)

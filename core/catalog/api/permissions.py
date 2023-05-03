from rest_framework.permissions import BasePermission

# see account `GlobalPermissions`
DOWNLOAD_MASTER_PERMISSION = "account.api_master_download"


class DownloadMasterPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(DOWNLOAD_MASTER_PERMISSION)

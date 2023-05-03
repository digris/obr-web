import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from catalog.api import permissions
from catalog.models import Master
from catalog.utils import get_signed_master_url
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class MasterDownloadView(
    APIView,
):
    permission_classes = [
        permissions.DownloadMasterPermission,
    ]

    @staticmethod
    @extend_schema(
        methods=["GET"],
        operation_id="catalog_master_download",
        description="""Returns (signed) URL to download the master file.""",
        responses={
            302: None,
        },
    )
    def get(request, uid):
        master = get_object_or_404(Master, media__uid=uid)

        url = get_signed_master_url(master)

        return HttpResponseRedirect(url)

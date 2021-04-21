import logging
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class SPAIndexView(TemplateView):
    template_name = "spa/index.html"
    path = ""

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

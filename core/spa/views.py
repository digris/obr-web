import logging

from django.http import Http404
from django.views.generic import TemplateView, View

logger = logging.getLogger(__name__)


class SPAIndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class SPA404View(View):
    def dispatch(self, request, *args, **kwargs):
        raise Http404()

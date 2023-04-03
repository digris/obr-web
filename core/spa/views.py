import logging

from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, View

from broadcast.utils import get_current_media

logger = logging.getLogger(__name__)


@method_decorator([never_cache], name="dispatch")
class SPAIndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_media = get_current_media()

        color = [220, 220, 220]

        if current_media:
            try:
                color = current_media.releases.first().image.rgb
            except:  # noqa: E722,S110
                pass

        context.update(
            {
                "color": color,
            }
        )

        return context


class SPA404View(View):
    def dispatch(self, request, *args, **kwargs):
        raise Http404()

from django.http import HttpResponse

from scalar_py import (
    CustomOptions,
    Options,
    ServerOptions,
    Spec,
    api_reference_html,
    get_base_path_from_spec,
)


def api_docs(request):
    spec_url = "http://localhost:8080/api/v1/schema-json/"
    base_path = get_base_path_from_spec(spec_url)

    opts = Options(
        spec=Spec(url=spec_url),
        custom_options=CustomOptions(
            page_title="My API Docs (Django)",
        ),
        servers=[
            ServerOptions(
                url="https://openbroadcast.ch",
                description="LIVE",
            ),
        ],
        pathRouting={"basePath": base_path} if base_path else None,
        hideDownloadButton=True,
        hiddenClients=True,
    )

    html = api_reference_html(opts)
    return HttpResponse(html)

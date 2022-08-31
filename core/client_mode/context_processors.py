def client_mode(request):

    ctx = {}

    if hasattr(request, "client_mode_app"):
        ctx.update(
            {
                "client_mode_app": request.client_mode_app,
            }
        )

    return ctx

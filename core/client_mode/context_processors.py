def client_mode(request):
    ctx = {}

    if hasattr(request, "client_mode"):
        ctx.update(
            {
                "client_mode": request.client_mode,
            }
        )

    return ctx

def geolocation(request):

    ctx = {}

    if hasattr(request, "geolocation_country"):
        ctx.update(
            {
                "geolocation_country": request.geolocation_country,
            }
        )

    if hasattr(request, "geolocation_city"):
        ctx.update(
            {
                "geolocation_city": request.geolocation_city,
            }
        )

    if hasattr(request, "geolocation_coordinates"):
        ctx.update(
            {
                "geolocation_coordinates": request.geolocation_coordinates,
            }
        )

    return ctx

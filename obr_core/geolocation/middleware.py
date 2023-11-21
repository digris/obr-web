from django.conf import settings

COUNTRY_HEADER = "X-Client-Geo-Location-Region"
CITY_HEADER = "X-Client-Geo-Location-City"
COORDINATES_HEADER = "X-Client-Geo-Location-Coordinates"

try:
    COUNTRY_OVERRIDE = settings.GEOLOCATION_COUNTRY_OVERRIDE
except AttributeError:
    COUNTRY_OVERRIDE = False


class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.geolocation_country = request.headers.get(COUNTRY_HEADER)
        request.geolocation_city = request.headers.get(CITY_HEADER)
        request.geolocation_coordinates = request.headers.get(COORDINATES_HEADER)

        if COUNTRY_OVERRIDE:
            request.geolocation_country = COUNTRY_OVERRIDE

        response = self.get_response(request)
        return response

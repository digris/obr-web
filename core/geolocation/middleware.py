# -*- coding: utf-8 -*-
COUNTRY_HEADER = "X-Client-Geo-Location-Region"
CITY_HEADER = "X-Client-Geo-Location-City"
COORDINATES_HEADER = "X-Client-Geo-Location-Coordinates"


class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.geolocation_country = request.headers.get(COUNTRY_HEADER)
        request.geolocation_city = request.headers.get(CITY_HEADER)
        request.geolocation_coordinates = request.headers.get(COORDINATES_HEADER)

        response = self.get_response(request)
        return response

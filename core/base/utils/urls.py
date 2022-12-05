from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

url_validator = URLValidator()


def get_absolute_url(request, url):
    try:
        url_validator(url)
        return url
    except ValidationError:
        return f"{request.scheme}://{request.get_host()}{url}"

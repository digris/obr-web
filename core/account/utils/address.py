from django_countries import countries


def get_countries():
    return [{"iso2_code": c[0], "name": c[1]} for c in countries]

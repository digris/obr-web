from django.conf import settings


BUCKET = getattr(settings, "GS_BUCKET_NAME")
URL = getattr(settings, "IMAGE_RESIZER_ENDPOINT", None)
DEFAULT_RESIZE_KIND = "scale"

IMAGE_WIDTH_SET = [120, 240, 360, 600, 900, 1200, 1800, 2400]
DEFAULT_RATIO = 16 / 10


def get_resized_url(
    file,
    width,
    height,
    kind,
):

    if not URL:
        return file.url

    # pylint: disable=consider-using-f-string
    url = "{endpoint}{kind}/{width}x{height}/{bucket}/{filename}".format(
        endpoint=URL,
        bucket=BUCKET,
        kind=kind,
        width=width,
        height=height,
        filename=file.name,
    )

    return url


def get_image_set(
    file,
    ratio=None,
    kind=None,
):
    ratio = ratio or DEFAULT_RATIO
    kind = kind or DEFAULT_RESIZE_KIND
    for width in IMAGE_WIDTH_SET:
        height = int(width / ratio)
        yield {
            "width": width,
            "height": height,
            "url": get_resized_url(file, width, height, kind),
        }

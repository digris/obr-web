import io

from PIL import Image, PngImagePlugin
from colorthief import ColorThief

RESIZE_TO = 100


# https://stackoverflow.com/questions/42671252/python-pillow-valueerror-decompressed-data-too-large
PngImagePlugin.MAX_TEXT_CHUNK = 4 * (1024 ** 2)


def read_as_image(file):
    image = Image.open(file)
    # fp.close()
    return image


def resize_image(img, size=100):
    ratio = img.height / img.width
    w, h = int(size), int(size * ratio)
    resized = img.resize((w, h))
    return resized


def image_as_fp(img):
    fp = io.BytesIO()
    try:
        img.save(fp, "png")
        fp.seek(0)
        return fp
    except OSError:
        return None


def extract_colors(file, num_colors=2):

    img = read_as_image(file=file.file)
    img = resize_image(img=img)

    try:
        fp = image_as_fp(img=img)
    except ValueError:
        return None, None

    if not fp:
        return None, None

    ct = ColorThief(fp)
    color = ct.get_color(quality=1)
    palette = ct.get_palette(color_count=num_colors, quality=1)

    return color, palette

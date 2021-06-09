import io
from PIL import Image
from colorthief import ColorThief

RESIZE_TO = 100


def read_as_image(file):
    fp = file
    image = Image.open(fp)
    fp.close()
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
    except OSError as e:
        print("e", e)
        return None


def extract_colors(file, num_colors=2):

    img = read_as_image(file=file.file)
    img = resize_image(img=img)
    fp = image_as_fp(img=img)

    if not fp:
        return None, None

    ct = ColorThief(fp)
    color = ct.get_color(quality=1)
    palette = ct.get_palette(color_count=num_colors, quality=1)

    return color, palette

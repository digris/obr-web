import settings from "@/settings";

const RESIZER_IMAGE_WITHS = [48, 72, 96, 120, 240, 280, 360, 600, 800, 1200, 1800];
const RESIZER_MAX_WIDTH = 1800;

const { IMAGE_RESIZER_ENDPOINT } = settings;

const getImageSrc = (image: any, size = 800) => {
  const resizeSize = RESIZER_IMAGE_WITHS.find((s) => s >= size) || RESIZER_MAX_WIDTH;

  // @ts-ignore
  if (image && image.path) {
    // @ts-ignore
    return `${IMAGE_RESIZER_ENDPOINT}crop/${resizeSize}x${resizeSize}/${image.path}`;
  }
  return null;
};

const getImageColor = (image: any) => {
  // @ts-ignore
  if (image && image.rgb) {
    // @ts-ignore
    return image.rgb;
  }
  return null;
};

const preloadImage = async (image: any, size = 800) => {
  if (!image) {
    return;
  }
  const src = getImageSrc(image, size);
  if (src) {
    const img = new Image();
    // img.onload = (e) => {
    //   console.debug("onload", e);
    // };
    img.src = src;
  }
};

export { getImageColor, getImageSrc, preloadImage };

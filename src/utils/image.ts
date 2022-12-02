import settings from "@/settings";

const { IMAGE_RESIZER_ENDPOINT } = settings;

const getImageSrc = (image: any, size = 800) => {
  // @ts-ignore
  if (image && image.path) {
    // @ts-ignore
    return `${IMAGE_RESIZER_ENDPOINT}crop/${size}x${size}/${image.path}`;
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

export { getImageSrc, getImageColor, preloadImage };

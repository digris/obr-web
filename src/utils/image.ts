import settings from "@/settings";

const { IMAGE_RESIZER_ENDPOINT } = settings;

const getImageSrc = (image: object, size = 800) => {
  // @ts-ignore
  if (image && image.path) {
    // @ts-ignore
    return `${IMAGE_RESIZER_ENDPOINT}crop/${size}x${size}/${image.path}`;
  }
  return null;
};

const getImageColor = (image: object) => {
  // @ts-ignore
  if (image && image.rgb) {
    // @ts-ignore
    return image.rgb;
  }
  return null;
};

export { getImageSrc, getImageColor };

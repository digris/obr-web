import settings from '@/settings';

const { IMAGE_RESIZER_URL } = settings;

const getImageSrc = (image: object, size: number = 240) => {
  // @ts-ignore
  if (image && image.path) {
    // @ts-ignore
    return `${IMAGE_RESIZER_URL}crop/${size}x${size}/${image.path}`;
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

// eslint-disable-next-line import/prefer-default-export
export { getImageSrc, getImageColor };
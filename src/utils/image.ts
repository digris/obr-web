import settings from '@/settings';

const { IMAGE_RESIZER_URL } = settings;

const getImageSrc = (obj: object, size: number = 240) => {
  // @ts-ignore
  console.debug('obj', obj, obj.image);
  // @ts-ignore
  if (obj.image && obj.image.path) {
    // @ts-ignore
    return `${IMAGE_RESIZER_URL}crop/${size}x${size}/${obj.image.path}`;
  }
  return null;
};

// eslint-disable-next-line import/prefer-default-export
export { getImageSrc };

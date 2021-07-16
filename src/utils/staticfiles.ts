import settings from '@/settings';

const { STATIC_URL } = settings;

// eslint-disable-next-line arrow-body-style
const getStaticSrc = (path: string) => {
  return `${STATIC_URL}${path}`;
};

export { getStaticSrc };

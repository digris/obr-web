import settings from '@/settings';

const { MEDIA_ENDPOINTS } = settings;

const getDashUrl = (media: object) => {
  // @ts-ignore
  console.debug('media', media);
  // @ts-ignore
  // const dummyUuids: Array = ['F001', 'F002', 'F003'];
  // const uid = dummyUuids[Math.floor(Math.random() * dummyUuids.length)];
  const { uid } = media;
  return `${MEDIA_ENDPOINTS.dash}${uid}/dash/manifest.mpd`;
};

// eslint-disable-next-line import/prefer-default-export
export { getDashUrl };

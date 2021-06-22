import settings from '@/settings';
import { getMediaFormat } from '@/utils/browser';

const { DEBUG, MEDIA_ENDPOINTS } = settings;

const SUFFIX_MAP = {
  hls: '/hls/manifest.m3u8',
  dash: '/dash/manifest.mpd',
};

export enum MediaSuffix {
  HLS = 'hls',
  DASH = 'dash',
}

const getSuffix = (format: string) => {
  // @ts-ignore
  return SUFFIX_MAP[format];
};

const getMediaUrl = (media: object) => {
  const mediaFormat = getMediaFormat();
  console.debug('mediaFormat', mediaFormat);
  const suffix = getSuffix(mediaFormat);
  console.debug('suffix', suffix);
  if (DEBUG) {
    const dummyUuids: Array<string> = ['F001', 'F001'];
    const uid = dummyUuids[Math.floor(Math.random() * dummyUuids.length)];
    // return `${MEDIA_ENDPOINTS.dash}${uid}/dash/manifest.mpd`;
    return `${MEDIA_ENDPOINTS.dash}${uid}${suffix}`;
  }
  // @ts-ignore
  // const dummyUuids: Array = ['F001', 'F002', 'F003'];
  // const uid = dummyUuids[Math.floor(Math.random() * dummyUuids.length)];
  const { uid } = media;
  return `${MEDIA_ENDPOINTS.dash}${uid}${suffix}`;
};

// eslint-disable-next-line import/prefer-default-export
export { getMediaUrl };

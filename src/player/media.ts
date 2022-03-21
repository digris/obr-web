import settings from "@/settings";
import { getMediaFormat } from "@/utils/browser";

const { MEDIA_ENDPOINTS } = settings;

const SUFFIX_MAP = {
  hls: "/hls/manifest.m3u8",
  dash: "/dash/manifest.mpd",
};

export enum MediaSuffix {
  HLS = "hls",
  DASH = "dash",
}

const getSuffix = (format: string) => {
  // @ts-ignore
  return SUFFIX_MAP[format];
};

const getMediaUrl = (media: object) => {
  const mediaFormat = getMediaFormat();
  const suffix = getSuffix(mediaFormat);
  // if (DEBUG) {
  //   const dummyUuids: Array<string> = ['556CCC59', '556CCC59', '556CCC59'];
  //   const uid = dummyUuids[Math.floor(Math.random() * dummyUuids.length)];
  //   return `${MEDIA_ENDPOINTS.dash}${uid}${suffix}`;
  // }
  // @ts-ignore
  const { uid } = media;
  return `${MEDIA_ENDPOINTS.dash}${uid}${suffix}`;
};

export { getMediaUrl };

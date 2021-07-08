import settings from '@/settings';
import eventBus from '@/eventBus';
import { getMediaFormat } from '@/utils/browser';

const { STREAM_ENDPOINTS } = settings;

export enum MediaSuffix {
  HLS = 'hls',
  DASH = 'dash',
}

const getUrl = (format: string) => {
  // @ts-ignore
  return STREAM_ENDPOINTS[format];
};

const getStreamUrl = (noCache: boolean = true) => {
  const mediaFormat = getMediaFormat();
  let url = getUrl(mediaFormat);
  if (noCache) {
    url = `${url}?${Date.now()}`;
  }
  return url;
};

const playStream = (startTime: number = -10) => {
  const url = getStreamUrl(true);
  const event = {
    do: 'play',
    url,
    startTime,
  };
  eventBus.emit('player:controls', event);
};

export { getStreamUrl, playStream };

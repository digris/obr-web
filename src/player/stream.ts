import settings from "@/settings";
import { getStreamMediaFormat } from "@/utils/browser";

const { STREAM_ENDPOINTS } = settings;

const getUrl = (format: string) => {
  // return "http://164.92.244.52:8080/live.m3u8";
  return "https://stream-abr.next.openbroadcast.ch/hls/manifest.m3u8";
  // TODO: this is just temporary!
  if (format === "hls") {
    return "https://stream-abr.next.openbroadcast.ch/hls/manifest.m3u8";
  }
  // @ts-ignore
  return STREAM_ENDPOINTS[format];
};

const getStreamUrl = (noCache = true) => {
  const mediaFormat = getStreamMediaFormat();
  // const mediaFormat = "hls";
  let url = getUrl(mediaFormat);
  if (noCache) {
    url = `${url}?${Date.now()}`;
  }
  return url;
};

export { getStreamUrl };

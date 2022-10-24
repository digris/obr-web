import settings from "@/settings";
import { getStreamMediaFormat } from "@/utils/browser";

const { STREAM_ENDPOINTS } = settings;

const getUrl = (format: string) => {
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

// import { computed } from "vue";
// import { useWindowSize } from "@vueuse/core";
import Bowser from "bowser";

import settings from "@/settings";

const parser = Bowser.getParser(window.navigator.userAgent);
const osName = parser.getOSName(true);
const browserName = parser.getBrowserName(true);
const browserPlatform = parser.getPlatformType(true);

// console.debug("browserPlatform", browserPlatform);

const useDevice = () => {
  // const { width, height } = useWindowSize();
  const isMobile = browserPlatform !== "desktop";
  const isDesktop = browserPlatform === "desktop";
  const isIos = osName === "ios";
  const isSafari = browserName === "safari";
  const isApp = settings.CLIENT_MODE === "app";
  const isWeb = !isApp;
  return {
    isMobile,
    isDesktop,
    isIos,
    isSafari,
    isApp,
    isWeb,
    osName,
    browserName,
    // windowSize: { width, height },
  };
};

export { useDevice };

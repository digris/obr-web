// import { computed } from "vue";
// import { useWindowSize } from "@vueuse/core";
import { computed } from "vue";
import Bowser from "bowser";
import log from "loglevel";
import { coerce as semverCoerce } from "semver";
import { storeToRefs } from "pinia";

import settings from "@/settings";
import { useUiStore } from "@/stores/ui";

type AppVersion = {
  major: number;
  minor: number;
  patch: number;
};

const parseAppUA = (ua: string): null | AppVersion => {
  if (!ua.toLowerCase().startsWith("obr-app-ios/")) {
    return null;
  }
  const semVer = semverCoerce(ua.substring(11));
  if (!semVer) {
    return null;
  }
  const { major, minor, patch } = semVer;
  return { major, minor, patch };
};

const parser = Bowser.getParser(window.navigator.userAgent);
const osName = parser.getOSName(true);
const browserName = parser.getBrowserName(true);
const browserPlatform = parser.getPlatformType(true);

log.debug("Device info", { parser, osName, browserName, browserPlatform });

const useDevice = () => {
  const isMobile = browserPlatform !== "desktop";
  const isDesktop = browserPlatform === "desktop";
  const isIos = osName === "ios";
  const isAndroid = osName === "android";
  const isSafari = browserName === "safari";
  const isApp = settings.CLIENT_MODE === "app";
  const appVersion = isApp ? parseAppUA(parser.getUA()) : null;
  const isWeb = !isApp;

  const { vpWidth, vpHeight } = storeToRefs(useUiStore());
  const isSmallScreen = computed(() => {
    return vpWidth.value <= 720;
  });

  return {
    isMobile,
    isDesktop,
    isIos,
    isAndroid,
    isSafari,
    isApp,
    appVersion,
    isWeb,
    osName,
    browserName,
    uaParser: parser,
    //
    vpWidth,
    vpHeight,
    isSmallScreen,
  };
};

export { useDevice };

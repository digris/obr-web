// import { computed } from "vue";
// import { useWindowSize } from "@vueuse/core";
import { computed } from "vue";
import Bowser from "bowser";
import { storeToRefs } from "pinia";

import settings from "@/settings";
import { useUiStore } from "@/stores/ui";

const parser = Bowser.getParser(window.navigator.userAgent);
const osName = parser.getOSName(true);
const browserName = parser.getBrowserName(true);
const browserPlatform = parser.getPlatformType(true);

const useDevice = () => {
  const isMobile = browserPlatform !== "desktop";
  const isDesktop = browserPlatform === "desktop";
  const isIos = osName === "ios";
  const isSafari = browserName === "safari";
  const isApp = settings.CLIENT_MODE === "app";
  const isWeb = !isApp;

  const { vpWidth, vpHeight } = storeToRefs(useUiStore());
  const isSmallScreen = computed(() => {
    return vpWidth.value <= 720;
  });

  return {
    isMobile,
    isDesktop,
    isIos,
    isSafari,
    isApp,
    isWeb,
    osName,
    browserName,
    //
    vpWidth,
    vpHeight,
    isSmallScreen,
  };
};

export { useDevice };

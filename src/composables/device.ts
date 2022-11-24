import { computed } from "vue";
import { useWindowSize } from "@vueuse/core";
import Bowser from "bowser";
import settings from "@/settings";

const parser = Bowser.getParser(window.navigator.userAgent);
const osName = parser.getOSName(true);

const useDevice = () => {
  const { width, height } = useWindowSize();
  const isMobile = computed(() => width.value && width.value < 721);
  const isDesktop = computed(() => !isMobile.value);
  const isIos = osName === "ios";
  const isApp = settings.CLIENT_MODE === "app";
  const isWeb = !isApp;
  return {
    isMobile,
    isDesktop,
    isIos,
    isApp,
    isWeb,
    windowSize: { width, height },
  };
};

export { useDevice };

import { computed } from "vue";
import { useWindowSize } from "@vueuse/core";
import settings from "@/settings";

const useDevice = () => {
  const { width, height } = useWindowSize();
  const isMobile = computed(() => {
    return width.value && width.value < 721;
  });
  const isDesktop = computed(() => {
    return !isMobile.value;
  });
  // @ts-ignore
  // const isWeb = !window?.webkit?.messageHandlers?.appBridge;
  // const isApp = !isWeb;
  const isApp = settings.CLIENT_MODE === "app";
  const isWeb = !isApp;
  return {
    isMobile,
    isDesktop,
    isApp,
    isWeb,
    windowSize: { width, height },
  };
};

export { useDevice };

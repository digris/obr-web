import { computed } from "vue";
import { useWindowSize } from "@vueuse/core";

const useDevice = () => {
  const { width, height } = useWindowSize();
  const isMobile = computed(() => {
    return width.value && width.value < 721;
  });
  const isDesktop = computed(() => {
    return !isMobile.value;
  });
  // @ts-ignore
  const isWeb = !window?.webkit?.messageHandlers?.appBridge;
  const isApp = !isWeb;
  return {
    isMobile,
    isDesktop,
    isWeb,
    isApp,
    windowSize: { width, height },
  };
};

export { useDevice };

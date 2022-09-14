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
  return {
    isMobile,
    isDesktop,
    windowSize: { width, height },
  };
};

export { useDevice };

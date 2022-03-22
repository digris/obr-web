import { computed } from "vue";
import { useWindowSize } from "@vueuse/core";

const useDevice = () => {
  const { width, height } = useWindowSize();
  const isMobile = computed(() => {
    return width.value && width.value < 500;
  });
  return {
    isMobile,
    windowSize: { width, height },
  };
};

export { useDevice };

import { computed } from "vue";

import { useDevice } from "@/composables/device";

const useIconSize = (scale = 1) => {
  const { isSmallScreen, isApp } = useDevice();
  const defaultIconSize = computed(() => {
    if (isApp) {
      return 40;
    }
    if (isSmallScreen.value) {
      return 40;
    }
    return 48;
  });
  const defaultIconStrokeWidth = computed(() => {
    if (isApp) {
      return 2.5;
    }
    if (isSmallScreen.value) {
      return 2.5;
    }
    return 3;
  });
  const iconSize = computed(() => {
    return defaultIconSize.value * scale;
  });
  const iconStrokeWidth = computed(() => {
    return defaultIconStrokeWidth.value * scale;
  });
  return {
    defaultIconSize,
    defaultIconStrokeWidth,
    iconSize,
    iconStrokeWidth,
  };
};

export { useIconSize };

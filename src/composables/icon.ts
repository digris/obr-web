import { computed } from "vue";

import { useDevice } from "@/composables/device";

const useIconSize = (scale = 1) => {
  const { isDesktop } = useDevice();
  const defaultIconSize = computed(() => {
    return isDesktop.value ? 48 : 40;
  });
  const iconSize = computed(() => {
    return defaultIconSize.value * scale;
  });
  return {
    defaultIconSize,
    iconSize,
  };
};

export { useIconSize };

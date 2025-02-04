<script lang="ts">
import { computed, defineComponent } from "vue";

import { useSettings } from "@/composables/settings";

export default defineComponent({
  props: {
    value: {
      type: Object,
      default: () => {},
    },
    position: {
      type: String,
      default: "absolute",
    },
    alwaysVisible: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const { userSettings } = useSettings();
    const isVisible = computed(() => {
      if (props.alwaysVisible) {
        return true;
      }
      return userSettings.value?.debugEnabled;
    });
    return {
      isVisible,
      userSettings,
    };
  },
});
</script>

<template>
  <div
    v-if="isVisible"
    class="debug-panel"
    :style="{
      position,
    }"
  >
    <pre v-text="value" />
    <slot />
  </div>
</template>

<style lang="scss" scoped>
.debug-panel {
  padding: 6px;
  font-weight: 300;
  font-size: 12px;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
}
</style>

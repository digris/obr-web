<script lang="ts">
import { computed, defineComponent } from "vue";

import Radio from "@/components/broadcast/radio/Radio.vue";
import RadioMobile from "@/components/broadcast/radio/RadioMobile.vue";
import { useDevice } from "@/composables/device";

export default defineComponent({
  setup() {
    const { isDesktop } = useDevice();
    const component = computed(() => {
      return isDesktop.value ? Radio : RadioMobile;
    });
    return {
      component,
    };
  },
});
</script>

<template>
  <component :is="component" />
</template>

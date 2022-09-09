<script lang="ts">
import { computed, defineComponent } from "vue";
import { useDevice } from "@/composables/device";
import Radio from "@/components/broadcast/radio/Radio.vue";
import RadioMobile from "@/components/broadcast/radio/RadioMobile.vue";

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

<style lang="scss" scoped></style>

<script lang="ts">
import { computed, defineComponent } from "vue";
import { useDevice } from "@/composables/device";
import Radio from "@/components/broadcast/Radio.vue";
import RadioMobile from "@/components/broadcast/RadioMobile.vue";

export default defineComponent({
  components: {
    Radio,
    RadioMobile,
  },
  setup() {
    const { isMobile } = useDevice();
    const component = computed(() => {
      return isMobile.value ? RadioMobile : Radio;
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

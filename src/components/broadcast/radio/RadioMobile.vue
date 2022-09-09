<script lang="ts">
import { computed, defineComponent } from "vue";
import { storeToRefs } from "pinia";
import { useTimeStore } from "@/stores/time";
import { useScheduleStore } from "@/stores/schedule";
import FlowMobile from "./flow/FlowMobile.vue";

export default defineComponent({
  components: {
    FlowMobile,
  },
  setup() {
    const { time } = storeToRefs(useTimeStore());
    const { items, current } = storeToRefs(useScheduleStore());
    const debugVars = {
      // time,
      current,
    };
    const offset = computed(() => {
      return 0;
    });
    const paginatedItems = computed(() => {
      const numItems = 20;
      return items.value.slice(offset.value, offset.value + numItems);
    });
    return {
      time,
      paginatedItems,
      debugVars,
    };
  },
});
</script>

<template>
  <div class="radio-mobile">
    <FlowMobile :items="paginatedItems" />
  </div>
</template>

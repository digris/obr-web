<script lang="ts">
import type { AnnotatedSchedule } from "@/stores/schedule";
import { ref, computed, defineComponent, onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useTimeStore } from "@/stores/time";
import { useScheduleStore } from "@/stores/schedule";
import eventBus from "@/eventBus";
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
    const debugOffset = ref(5);
    const offset = computed(() => {
      return debugOffset.value;
    });
    const paginatedItems = computed(() => {
      const numItems = 10;
      return items.value.slice(offset.value, offset.value + numItems);
    });
    const focusedItemKey = ref("");
    const onItemFocused = (item: AnnotatedSchedule) => {
      focusedItemKey.value = item.key;
    };
    const focusedItem = computed((): AnnotatedSchedule | null => {
      // NOTE: we use all items here (not paginatedItems)
      const item = items.value.find((i: AnnotatedSchedule) => i.key === focusedItemKey.value);
      return item ? item : null;
    });
    const focusNext = () => {
      eventBus.emit("radio:flow", "focusNext");
    };
    const focusPrevious = () => {
      eventBus.emit("radio:flow", "focusPrevious");
    };
    const releaseFocus = () => {
      eventBus.emit("radio:flow", "releaseFocus");
    };
    //
    onMounted(() => {
      setInterval(() => {
        if (debugOffset.value > 0) {
          debugOffset.value -= 1;
          eventBus.emit("radio:flow", "itemAdded");
          // setTimeout(() => {
          //   eventBus.emit("radio:flow", "update");
          // }, 1000)
        }
      }, 5000);
    });
    return {
      time,
      paginatedItems,
      debugOffset,
      debugVars,
      onItemFocused,
      focusedItem,
      //
      focusNext,
      focusPrevious,
      releaseFocus,
    };
  },
});
</script>

<template>
  <div class="radio-mobile">
    <FlowMobile :items="paginatedItems" @on-item-focused="onItemFocused" />
    <div>
      <!--
      <input type="number" min="0" v-model="debugOffset" />
      <br />
      -->
      <button @click.prevent="focusPrevious" v-text="`PREV`" />
      <button @click.prevent="focusNext" v-text="`NEXT`" />
      <button @click.prevent="releaseFocus" v-text="`FOLLOW`" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.radio-mobile {
  input,
  button {
    padding: 6px;
  }
}
</style>

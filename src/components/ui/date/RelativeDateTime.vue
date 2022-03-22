<script lang="ts">
import {
  computed,
  defineComponent,
  ref,
  onMounted,
  onUnmounted,
  onActivated,
  onDeactivated,
} from "vue";
import { DateTime } from "luxon";

const TIME_UPDATE_INTERVAL = 60000;

export default defineComponent({
  props: {
    dateTime: {
      type: DateTime,
      required: true,
    },
  },
  setup(props) {
    const now = ref(DateTime.now());
    const isToday = computed(() => {
      return props.dateTime.hasSame(now.value, "day");
    });
    const timeDisplay = computed(() => {
      if (isToday.value) {
        return `Heute ${props.dateTime.toFormat("HH:mm")}`;
      }
      return props.dateTime.setLocale("de-CH").toRelativeCalendar();
    });
    let interval: ReturnType<typeof setInterval>;
    const startInterval = () => {
      interval = setInterval(() => {
        now.value = DateTime.now();
      }, TIME_UPDATE_INTERVAL);
    };
    const stopInterval = () => {
      if (interval) {
        clearInterval(interval);
      }
    };
    onMounted(() => startInterval());
    onActivated(() => startInterval());
    onUnmounted(() => stopInterval());
    onDeactivated(() => stopInterval());
    return {
      timeDisplay,
    };
  },
});
</script>

<template>
  <span class="date-or-time">
    <slot name="default"></slot>
    {{ timeDisplay }}
  </span>
</template>

<style lang="scss" scoped>
.date-or-time {
  display: inline-flex;
}
</style>

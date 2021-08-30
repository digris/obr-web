<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { DateTime } from 'luxon';

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
      return (props.dateTime.hasSame(now.value, 'day'));
    });
    /*
    const timeFormat = computed(() => {
      const dt = props.dateTime;
      if (dt.hasSame(now.value, 'day')) {
        return 'HH:mm';
      }
      if (dt.hasSame(now.value, 'month')) {
        console.debug(dt.toRelativeCalendar());
        return 'yyyy-LL-dd';
      }
      return 'yyyy-LL-dd';
    });
    */
    const timeDisplay = computed(() => {
      if (isToday.value) {
        return `Heute ${props.dateTime.toFormat('HH:mm')}`;
      }
      return props.dateTime.setLocale('de-CH').toRelativeCalendar();
    });
    setInterval(() => {
      now.value = DateTime.now();
    }, 5000);
    return {
      timeDisplay,
    };
  },
});
</script>

<template>
  <span
    class="date-or-time"
  >
    <slot
      name="default"
    ></slot>
    {{ timeDisplay }}
  </span>
</template>

<style lang="scss" scoped>
.date-or-time {
  display: inline-flex;
}
</style>

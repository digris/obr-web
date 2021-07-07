<script lang="ts">
import { computed, defineComponent } from 'vue';
import { DateTime } from 'luxon';

export default defineComponent({
  props: {
    value: {
      type: [String, DateTime],
      required: true,
    },
    displayDate: {
      type: Boolean,
      default: true,
    },
    displayTime: {
      type: Boolean,
      default: true,
    },
  },
  setup(props) {
    const parsedValue = computed(() => {
      console.debug(props.value, typeof props.value);
      if (typeof props.value === 'string') {
        return DateTime.fromISO(props.value);
      }
      return props.value;
    });
    const dateDisplay = computed(() => {
      if (!props.displayDate) {
        return null;
      }
      // @ts-ignore
      return parsedValue.value.setLocale('de-ch').toLocaleString(DateTime.DATE_SHORT);
    });
    const timeDisplay = computed(() => {
      if (!props.displayTime) {
        return null;
      }
      // @ts-ignore
      return parsedValue.value.setLocale('de-ch').toLocaleString(DateTime.TIME_24_SIMPLE);
    });
    return {
      dateDisplay,
      timeDisplay,
    };
  },
});
</script>

<template>
  <span
    class="datetime"
  >
    <span
      v-if="dateDisplay"
      class="datetime__date"
    >{{ dateDisplay }}</span>
    <span
      v-if="(dateDisplay && timeDisplay)"
      class="datetime__separator"
    ></span>
    <span
      v-if="timeDisplay"
      class="datetime__time"
    >{{ timeDisplay }}</span>
  </span>
</template>

<style lang="scss" scoped>
.datetime {
  display: inline-flex;
  &__date,
  &__time {
    white-space: nowrap;
  }
  &__separator {
    padding-left: 0.5rem;
  }
}
</style>

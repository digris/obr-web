<script lang="ts" setup>
import { computed } from "vue";
import { DateTime } from "luxon";
import { isString } from "lodash-es";

interface Props {
  value: string | DateTime;
  displayDate?: boolean;
  displayTime?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  displayDate: true,
  displayTime: true,
});

const parsedValue = computed(() => {
  if (isString(props.value)) {
    return DateTime.fromISO(props.value);
  }
  return props.value;
});
const dateDisplay = computed(() => {
  if (!props.displayDate) {
    return null;
  }
  return parsedValue.value.setLocale("de-ch").toLocaleString(DateTime.DATE_SHORT);
});
const timeDisplay = computed(() => {
  if (!props.displayTime) {
    return null;
  }
  return parsedValue.value.setLocale("de-ch").toLocaleString(DateTime.TIME_24_SIMPLE);
});
</script>

<template>
  <span class="datetime">
    <span v-if="dateDisplay" class="datetime__date">{{ dateDisplay }}</span>
    <span v-if="dateDisplay && timeDisplay" class="datetime__separator"></span>
    <span v-if="timeDisplay" class="datetime__time">{{ timeDisplay }}</span>
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

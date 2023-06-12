<script lang="ts" setup>
import { computed, onActivated, onDeactivated, onMounted, onUnmounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { DateTime } from "luxon";

const TIME_UPDATE_INTERVAL = 60000;

const props = defineProps<{
  dateTime: DateTime;
}>();

const { locale, t } = useI18n();

const now = ref(DateTime.now());
const isToday = computed(() => props.dateTime.hasSame(now.value, "day"));
const timeDisplay = computed(() => props.dateTime.toFormat("HH:mm"));
const dateDisplay = computed(() => {
  if (isToday.value) {
    return t("datetime.today");
  }
  return props.dateTime.setLocale(locale.value).toLocaleString(DateTime.DATE_SHORT);
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

onMounted(startInterval);
onActivated(startInterval);
onUnmounted(stopInterval);
onDeactivated(stopInterval);
</script>

<template>
  <span class="datetime">
    <slot name="default"></slot>
    <span class="date" v-text="dateDisplay" />
    <span class="time" v-text="timeDisplay" />
  </span>
</template>

<style lang="scss" scoped>
.datetime {
  display: inline-flex;

  .date {
    text-transform: capitalize;
    margin-right: 0.5em;
  }
}
</style>

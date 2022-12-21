<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, ref, watch } from "vue";
import { DateTime } from "luxon";

import DatetInput from "@/components/ui/form/DatetInput.vue";

export type Time = {
  hour: number;
  minute: number;
};

export type Filter = {
  date: DateTime;
  time: Time;
};

export default defineComponent({
  components: {
    DatetInput,
  },
  props: {
    modelValue: {
      type: Object as PropType<Filter>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const minute = ref(0);
    const date = computed(() => {
      return props.modelValue.date;
    });
    const time = computed(() => {
      return props.modelValue.time;
    });
    const today = DateTime.now();
    const hour = ref(time.value?.hour ?? 7);
    const dateInput = ref(date.value.toISODate());
    const dateInputMin = "2019-01-01";
    const dateInputMax = computed(() => {
      return today.toISODate();
    });
    const userFilter = computed(() => {
      const filterDate = DateTime.fromISO(dateInput.value);
      const filterTime = {
        hour: hour.value,
        minute: minute.value,
      };
      return {
        date: filterDate,
        time: filterTime,
      };
    });
    const update = (value: Filter) => {
      emit("update:modelValue", value);
    };
    watch(() => userFilter.value, update);
    return {
      dateInput,
      dateInputMin,
      dateInputMax,
    };
  },
});
</script>

<template>
  <div>
    <div class="filter">
      <DatetInput v-model="dateInput" :min="dateInputMin" :max="dateInputMax" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.filter {
  position: relative;
  height: 38px;
  display: flex;
  min-width: 240px;

  > .date-input {
    width: 100%;

    :deep(> input) {
      width: 240px;
      padding: 0 0.5rem;
      font-size: 1rem;
      text-align: center;
      font-family: var(--font-family);
      border: 1px solid rgb(var(--c-dark) / 20%);
    }
  }
}
</style>

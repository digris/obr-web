<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, ref } from "vue";
import { watchDebounced } from "@vueuse/core";
import { DateTime } from "luxon";

import DateInput from "@/components/ui/form/DateInput.vue";

export type Filter = {
  date: DateTime;
};

export default defineComponent({
  components: {
    DateInput,
  },
  props: {
    modelValue: {
      type: Object as PropType<Filter>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const date = computed(() => {
      return props.modelValue.date;
    });
    const today = DateTime.now();
    const dateInput = ref(date.value.toISODate());
    const dateInputMin = "2019-01-01";
    const dateInputMax = computed(() => {
      return today.toISODate();
    });
    const userFilter = computed(() => {
      const filterDate = DateTime.fromISO(dateInput.value);
      return {
        date: filterDate,
      };
    });
    const update = (value: Filter) => {
      emit("update:modelValue", value);
    };
    watchDebounced(() => userFilter.value, update, { debounce: 200 });
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
      <DateInput v-model="dateInput" :min="dateInputMin" :max="dateInputMax" />
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

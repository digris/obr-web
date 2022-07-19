<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, ref, watch } from "vue";
import { range } from "lodash-es";
import { useI18n } from "vue-i18n";
import { DateTime } from "luxon";
import { zeroPad } from "@/utils/format";
import SelectInput from "@/components/ui/form/SelectInput.vue";

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
    SelectInput,
  },
  props: {
    modelValue: {
      type: Object as PropType<Filter>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const { locale } = useI18n();
    const minute = ref(0);
    const date = computed(() => {
      return props.modelValue.date;
    });
    const time = computed(() => {
      return props.modelValue.time;
    });
    const today = DateTime.now();
    const hour = ref(time.value?.hour ?? 7);
    const day = ref(date.value.day);
    const month = ref(date.value.month);
    const year = ref(date.value.year);
    // const day = ref(7);
    const dayOpts = computed(() => {
      // const date = props.modelValue.date;
      const base = date.value.startOf("month");
      const dayEnd = date.value.endOf("month").day;
      return range(0, dayEnd).map((n: number) => {
        const d = base.plus({ days: n });
        return {
          value: d.day,
          name: d.setLocale(locale.value).toFormat("dd / ccc"),
        };
      });
    });
    const monthOpts = computed(() => {
      const base = date.value.startOf("year");
      const monthEnd = date.value.endOf("year").month;
      // if (today.hasSame(date.value, "year")) {
      //   monthEnd = today.month;
      // }
      return range(0, monthEnd).map((n: number) => {
        const d = base.plus({ months: n });
        return {
          value: d.month,
          name: d.setLocale(locale.value).toLocaleString({ month: "short" }),
        };
      });
    });
    const yearOpts = computed(() => {
      const startYear = 2016;
      const endYear = DateTime.now().year;
      return range(endYear, startYear - 1).map((n: number) => {
        return {
          value: n,
          name: n,
        };
      });
    });
    const hourOpts = computed(() => {
      return range(0, 24).map((n: number) => {
        const h = n < 19 ? n + 6 : n - 18;
        return {
          value: h,
          name: `${zeroPad(h)}:00`,
        };
      });
    });
    const userFilter = computed(() => {
      const filterDate = DateTime.fromObject({
        day: day.value,
        month: month.value,
        year: year.value,
      });
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
      today,
      day,
      dayOpts,
      month,
      monthOpts,
      year,
      yearOpts,
      hour,
      hourOpts,
      userFilter,
    };
  },
});
</script>

<template>
  <div>
    <div class="filter">
      <SelectInput v-model="day" :options="dayOpts" />
      <SelectInput v-model="month" :options="monthOpts" />
      <SelectInput v-model="year" :options="yearOpts" />
      <SelectInput v-model="hour" :options="hourOpts" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.filter {
  position: relative;
  height: 48px;
  display: grid;
  grid-template-columns: 120px 120px 120px 120px;
  grid-column-gap: 0.5rem;
  > select {
    background: white;
    padding: 0 0.5rem;
  }
}
</style>

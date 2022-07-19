<script lang="ts">
import { defineComponent, ref, computed, onActivated, watch } from "vue";
import { useStore } from "vuex";
import { useRouteHash } from "@vueuse/router";
import { isEqual } from "lodash-es";
import Filter from "./Filter.vue";
import Emission from "./emission/Emission.vue";
import { DateTime } from "luxon";
import { zeroPad } from "@/utils/format";

const timeStrRegex = new RegExp("^#([0,1,2])([0-9]):([0-5])([0-9])$");

export default defineComponent({
  components: {
    Filter,
    Emission,
  },
  props: {
    date: {
      type: DateTime,
      required: true,
    },
    title: {
      type: String,
      default: "Program",
    },
    currentLinkToHome: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["navigate", "dateUpdate"],
  setup(props, { emit }) {
    const store = useStore();
    const emissions = computed(() => store.getters["program/emissions"]);
    const navigate = () => {
      emit("navigate");
    };
    const timeInFuture = computed(() => {
      return props.date > DateTime.now();
    });
    const timeStr = useRouteHash();
    const time = computed(() => {
      if (timeStrRegex.test(timeStr.value)) {
        const hour = parseInt(timeStr.value.substring(1, 3));
        const minute = parseInt(timeStr.value.substring(4, 6));
        return {
          hour: Math.min(hour, 23),
          minute: minute,
        };
      }
      return {
        hour: DateTime.now().startOf("hour").hour,
        minute: 0,
      };
    });
    const filter = ref({
      date: props.date,
      time: time.value,
    });
    const loadEmissions = async (date: DateTime) => {
      const dateStr = date.toISODate();
      await store.dispatch("program/loadEmissions", dateStr);
    };
    // onMounted(() => loadEmissions(props.date));
    onActivated(() => loadEmissions(props.date));
    watch(
      () => props.date,
      (newValue, oldValue) => {
        if (!isEqual(newValue, oldValue)) {
          loadEmissions(newValue);
        }
      }
    );
    watch(
      () => filter.value,
      (newValue, oldValue) => {
        if (!isEqual(newValue.time, oldValue.time)) {
          const t = newValue.time;
          timeStr.value = `#${zeroPad(t.hour)}:${zeroPad(t.minute)}`;
        }
        if (!isEqual(newValue.date, oldValue.date)) {
          emit("dateUpdate", newValue.date);
        }
      }
    );
    return {
      timeStr,
      timeInFuture,
      time,
      filter,
      emissions,
      navigate,
    };
  },
});
</script>
<template>
  <div class="program">
    <!--
    <pre v-text="{ timeStr, time, filter }" />
    -->
    <div class="header">
      <div class="title" v-text="title" />
      <div class="filter-container">
        <Filter class="filter" v-model="filter" />
      </div>
    </div>
    <div class="body">
      <div v-if="timeInFuture">
        <p>TIME IS IN FUTURE...</p>
      </div>
      <div class="emissions">
        <Emission
          v-for="(emission, index) in emissions"
          :key="`program-emission-${emission.uid}-${index}`"
          :emission="emission"
          :current-link-to-home="currentLinkToHome"
          @navigate="navigate"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";

.program {
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.header {
  border-bottom: 1px solid rgb(var(--c-gray-200));
  .title {
    @include container.default;
    @include typo.x-large;
    @include typo.bold;
    margin-top: 1.25rem;
    margin-bottom: 1.5rem;
  }
  .filter-container {
    padding: 0.5rem 0 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.body {
  flex-grow: 1;
  //overflow: scroll;
  min-height: 0; /* without min-height/height:0 flex:1 doesn't work */
  overflow: auto;
  .emissions {
    background: transparent;
  }
}
</style>

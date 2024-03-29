<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent, onActivated, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { DateTime } from "luxon";
import { storeToRefs } from "pinia";
import { isEqual } from "lodash-es";

import { useProgramStore } from "@/stores/program";

import Emission from "./emission/Emission.vue";
import Filter from "./Filter.vue";

export default defineComponent({
  components: {
    Filter,
    Emission,
  },
  props: {
    date: {
      type: Object as PropType<DateTime>,
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
    const { t } = useI18n();
    const { emissions } = storeToRefs(useProgramStore());
    const { loadEmissions } = useProgramStore();
    const navigate = () => {
      emit("navigate");
    };
    const timeInFuture = computed(() => {
      return props.date > DateTime.now();
    });
    const filter = ref({
      date: props.date,
    });

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
        if (!isEqual(newValue.date, oldValue.date)) {
          emit("dateUpdate", newValue.date);
        }
      }
    );
    return {
      t,
      timeInFuture,
      filter,
      emissions,
      navigate,
    };
  },
});
</script>
<template>
  <div class="program">
    <div class="header">
      <div class="title" v-text="title" />
      <div class="filter-container">
        <Filter class="filter" v-model="filter" />
      </div>
    </div>
    <div class="body">
      <div v-if="timeInFuture" class="invalid-date">
        <i18n-t keypath="program.timeInFuture.lead" tag="p" />
        <i18n-t keypath="program.timeInFuture.cta" tag="p">
          <router-link to="/program/" v-text="t('program.timeInFuture.ctaText')" />
        </i18n-t>
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
@use "@/style/elements/title";

.program {
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.header {
  border-bottom: 1px solid rgb(var(--c-dark) / 20%);

  .title {
    @include title.default;
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
  min-height: 0; /* without min-height/height:0 flex:1 doesn't work */
  overflow: auto;

  > .invalid-date {
    min-height: 4rem;
    margin-top: 4rem;
    margin-bottom: 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: var(--t-fs-large);

    a {
      text-decoration: underline;
    }
  }
}
</style>

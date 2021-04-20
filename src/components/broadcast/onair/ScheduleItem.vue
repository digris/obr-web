<script>
// import settings from '@/settings';
// import LazyImage from '@/components/UI/LazyImage.vue';
import { DateTime } from 'luxon';

import { computed } from 'vue';

export default {
  // components: { LazyImage },
  props: {
    isCurrent: {
      type: Boolean,
      default: false,
    },
    scheduleItem: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    // eslint-disable-next-line arrow-body-style
    const media = computed(() => {
      return props.scheduleItem ? props.scheduleItem.media : null;
    });
    const timeFormat = DateTime.TIME_WITH_SECONDS;
    return { media, timeFormat };
  },
};
</script>

<template>
  <div
    class="schedule-item"
    :class="{'is-current': isCurrent}"
  >
    <div
      v-if="media"
    >
      <h4>{{ media.name }}</h4>
      <small>UID: {{ media.uid }}</small>
    </div>
    <div
      class="timing"
    >
      <small
        class="label"
      >
        Airtime:
      </small>
      <span
        class="value"
      >
        {{ scheduleItem.timeStart.toLocaleString(timeFormat) }}
        -
        {{ scheduleItem.timeEnd.toLocaleString(timeFormat) }}
      </span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
.schedule-item {
  padding: 0.5rem;
  &.is-current {
    @include live-color.fg-inverse;
    @include live-color.bg-inverse;
  }
}
.mono {
  font-family: "Bitstream Vera Sans Mono", Monaco, "Courier New", Courier, monospace;
}
</style>

<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";
import { DateTime } from "luxon";
import { storeToRefs } from "pinia";

import Duration from "@/components/ui/time/Duration.vue";
import { useTimeStore } from "@/stores/time";
import type { Media } from "@/typings/api";

import MediaRow from "./MediaRow.vue";

export default defineComponent({
  components: {
    MediaRow,
    Duration,
  },
  props: {
    mediaSet: {
      // type: Array,
      type: Array as PropType<Array<Media>>,
      required: true,
    },
  },
  setup(props) {
    const { time } = storeToRefs(useTimeStore());
    const visibleMediaSet = computed(() => {
      return props.mediaSet.filter((m: any) => DateTime.fromISO(m.timeStart) < time.value);
    });
    const numHidden = computed(() => {
      return props.mediaSet.length - visibleMediaSet.value.length;
    });
    const nextMedia = computed(() => {
      return props.mediaSet.find((m: any) => DateTime.fromISO(m.timeStart) > time.value);
    });
    const nextStartInSeconds = computed(() => {
      if (!nextMedia.value) {
        return 0;
      }
      return time.value.diff(DateTime.fromISO(nextMedia.value.timeStart), "seconds").seconds;
    });
    return {
      time,
      visibleMediaSet,
      numHidden,
      nextStartInSeconds,
    };
  },
});
</script>

<template>
  <div class="media-set">
    <TransitionGroup name="list">
      <MediaRow
        v-for="(media, index) in visibleMediaSet"
        :emission-media="media"
        :key="`emission-media-${index}-${media.uid}`"
      />
    </TransitionGroup>
    <div class="feature-media" v-if="numHidden > 0">
      <Duration class="next-start" :seconds="nextStartInSeconds * -1" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";

.media-set {
  .media-row {
    &:not(&:first-child) {
      border-top: 1px solid rgb(var(--c-dark) / 20%);
    }
  }

  .feature-media {
    border-top: 1px solid rgb(var(--c-dark) / 20%);
    display: flex;
    align-items: center;
    justify-content: flex-start;
    color: rgb(var(--c-dark) / 20%);
    padding: 1rem 1rem 1rem calc(2rem + 48px);

    .next-start {
      @include typo.large;
    }

    @include responsive.bp-medium {
      padding: 1rem;
      justify-content: center;
    }
  }
}

.list-enter-active,
.list-leave-active {
  transition: opacity 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
}
</style>

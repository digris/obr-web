<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";
import { storeToRefs } from "pinia";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconProgram from "@/components/ui/icon/IconProgram.vue";
import type { AnnotatedSchedule } from "@/stores/schedule";
import { useTimeStore } from "@/stores/time";

import HistoryTime from "./station-time/HistoryTime.vue";
import StationTime from "./station-time/StationTime.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconProgram,
    StationTime,
    HistoryTime,
  },
  props: {
    item: {
      type: Object as PropType<AnnotatedSchedule>,
      required: false,
    },
  },
  emits: ["releaseFocus"],
  setup(props, { emit }) {
    const { time } = storeToRefs(useTimeStore());
    const isHistory = computed(() => {
      if (!props?.item?.dtEnd) {
        return false;
      }
      return props?.item?.dtEnd < time.value;
    });
    const releaseFocus = () => {
      emit("releaseFocus");
    };
    return {
      time,
      isHistory,
      releaseFocus,
    };
  },
});
</script>

<template>
  <div class="radio-header">
    <router-link class="program" :to="{ name: 'programRedirect' }">
      <CircleButton>
        <IconProgram color-var="--c-page-fg" />
      </CircleButton>
    </router-link>
    <div class="time">
      <transition name="time" mode="out-in">
        <HistoryTime v-if="isHistory && item?.dtStart" :time="item.dtStart" @click="releaseFocus" />
        <StationTime v-else />
      </transition>
    </div>
    <div class="time-shift" />
  </div>
</template>

<style lang="scss" scoped>
.radio-header {
  display: flex;
  align-items: center;
  justify-content: center;

  .program {
    height: 48px;
    width: 60px;
  }

  .time {
    flex-grow: 1;
  }

  .time-shift {
    width: 60px;
    opacity: 0;
  }
}

.time-enter-active {
  transition: opacity 500ms;
}

.time-enter-from {
  opacity: 0;
}

.time-leave-to {
  opacity: 0;
}
</style>

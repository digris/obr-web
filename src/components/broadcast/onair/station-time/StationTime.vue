<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
// import { playStream } from '@/player/stream';

import ToggleProgramButton from './ToggleProgramButton.vue';
import IconClose from '@/components/ui/icon/IconClose.vue';

const zeroPad = (n:number) => {
  return n > 9 ? `${n}` : `0${n}`;
};

export default defineComponent({
  components: {
    ToggleProgramButton,
    IconClose,
  },
  props: {
    timeOverwrite: {
      type: Object,
      required: false,
    },
  },
  emits: [
    'releaseFocus',
    'toggleProgram',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const time = computed(() => {
      if (props.timeOverwrite) {
        return props.timeOverwrite;
      }
      return store.getters['time/time'];
    });
    const hour = computed(() => {
      return zeroPad(time.value.hour);
    });
    const minute = computed(() => {
      return zeroPad(time.value.minute);
    });
    const second = computed(() => {
      return zeroPad(time.value.second);
    });
    const offset = computed(() => {
      return store.getters['time/offset'];
    });
    const releaseFocus = () => {
      emit('releaseFocus');
    };
    const toggleProgram = () => {
      emit('toggleProgram');
    };
    return {
      time,
      hour,
      minute,
      second,
      // isTimeshifted,
      offset,
      toggleProgram,
      releaseFocus,
    };
  },
});
</script>

<template>
  <div
    class="station-time"
  >
    <div
      class="actions"
    >
      <ToggleProgramButton
        @click.prevent="toggleProgram"
      />
    </div>
    <div
      class="container"
      :class="{
        'is-past': !!(timeOverwrite),
      }"
    >
      <div
        class="time"
        @click="releaseFocus"
      >
        <span
          class="hour"
          v-text="hour"
        />
        <span
          class="separator separator--minute"
          v-text="`:`"
        />
        <span
          class="minute"
          v-text="minute"
        />
        <!--
        <span
          class="separator separator--second"
        >:</span>
        <span
          class="second"
        >{{ second }}</span>
        -->
        <IconClose
          class="icon"
          :size="(36)"
          color="rgb(var(--c-page-fg-inverse))"
        />
      </div>
    </div>
    <div
      class="actions"
    >
    </div>
  </div>
</template>
<style lang="scss">
@keyframes pulsate {
  50% {
    opacity: 0;
  }
}
</style>
<style lang="scss" scoped>
@use "sass:math";
@use "@/style/base/live-color";
@use "@/style/elements/container";
$width: 200px;
$height: 48px;
.station-time {
  //@include container.default;
  display: grid;
  grid-template-columns: 48px 1fr 48px;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem 0 1rem;
  .actions {
    height: 48px;
  }
}
.container {
  @include live-color.fg;
  position: relative;
  display: inline-flex;
  grid-column-start: 2;
  align-items: center;
  justify-content: center;
  min-width: $width;
  height: 78px;
  user-select: none;
  .time {
    display: grid;
    //flex-grow: 1;
    grid-template-columns: 1em 0.5em 1em;
    align-items: center;
    justify-content: center;
    font-size: 64px;
    transition: background-color 20ms, color 100ms, font-size 200ms;
    > span {
      justify-self: center;
    }
    .hour,
    .minute,
    .second {
      font-weight: 600;
      font-size: 1em;
    }
    .separator {
      font-size: 0.5em;
      animation: pulsate 2s linear infinite;
    }
    .icon {
      display: none;
    }
  }
  &.is-past {
    .time {
      grid-template-columns: 1em 0.75em 1em 1em;
      background: yellow;
      font-size: 16px;
      padding: 0 32px;
      //height: 48px;
      border-radius: 24px;
      @include live-color.bg-inverse;
      @include live-color.fg-inverse;
      transition: background-color 1000ms, color 100ms 400ms, font-size 200ms;
      .separator {
        font-size: 1em;
      }
      .icon {
        display: flex;
        cursor: pointer;
        transition: stroke 1000ms;
      }
    }
  }
  .time-shift {
    @include live-color.fg;
    display: grid;
    grid-template-columns: 36px 1fr 36px;
    align-items: center;
    justify-content: center;
    min-width: $width;
    height: 3rem;
    border: 3px solid transparent;
    border-color: inherit;
    border-radius: math.div($height, 2);
    .offset {
      grid-column-start: 2;
      justify-self: center;
    }
  }
}
</style>

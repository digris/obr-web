<script lang="ts">
import { DateTime } from "luxon";
import { computed, defineComponent } from "vue";

import IconClose from "@/components/ui/icon/IconClose.vue";
import { zeroPad } from "@/utils/format";

export default defineComponent({
  components: {
    IconClose,
  },
  props: {
    time: {
      type: DateTime,
      required: true,
    },
  },
  setup(props) {
    const hour = computed(() => {
      return zeroPad(props.time.hour);
    });
    const minute = computed(() => {
      return zeroPad(props.time.minute);
    });
    return {
      hour,
      minute,
    };
  },
});
</script>

<template>
  <div class="history-time">
    <div class="bubble">
      <div class="time">
        <span class="hour" v-text="hour" />
        <span class="separator separator--minute" v-text="`:`" />
        <span class="minute" v-text="minute" />
      </div>
      <div class="icon">
        <IconClose :scale="0.825" color-var="--c-page-fg-inverse" />
      </div>
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
@use "@/style/base/live-color";

.history-time {
  display: flex;
  align-items: center;
  justify-content: center;

  .bubble {
    border-radius: 24px;
    @include live-color.bg-inverse;
    @include live-color.fg-inverse;

    transition: background-color 600ms, color 100ms 1ms, font-size 200ms;
    height: 48px;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    padding: 0 0 0 24px;
    display: flex;

    > .time {
      flex-grow: 1;
      display: grid;
      grid-template-columns: 20px 12px 20px;

      > span {
        justify-self: center;
      }

      .hour,
      .minute {
        font-weight: 600;
      }

      .separator {
        padding-top: 2px;
        font-size: 16px;
        animation: pulsate 2s linear infinite;
      }
    }

    .icon {
      cursor: pointer;
      width: 50px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
    }
  }
}
</style>

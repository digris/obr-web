<script lang="ts">
import { computed, defineComponent, onMounted } from "vue";
import { useStore } from "vuex";
import { useQueueControls } from "@/composables/queue";
import QueueMedia from "@/components/player/QueueMedia.vue";
import ShuffleControl from "./ShuffleControl.vue";
import IconCaret from "@/components/ui/icon/IconCaret.vue";
import Circle from "./button/Circle.vue";

export default defineComponent({
  components: {
    QueueMedia,
    ShuffleControl,
    IconCaret,
    Circle,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    bottom: {
      type: Number,
      default: 72,
    },
  },
  emits: ["close"],
  setup(props, { emit }) {
    const store = useStore();
    const { clearQueue } = useQueueControls();
    const mediaList = computed(() => store.getters["queue/media"]);
    // const currentIndex = computed(() => store.getters['queue/currentIndex']);
    const currentMedia = computed(() => store.getters["queue/currentMedia"]);
    const close = () => {
      emit("close");
    };
    onMounted(() => {
      document.addEventListener("keydown", (e) => {
        if (props.isVisible && e.code === "KeyX") {
          close();
        }
      });
    });
    return {
      close,
      mediaList,
      currentMedia,
      clearQueue,
    };
  },
});
</script>
<template>
  <transition name="fade">
    <div v-if="isVisible" @click="close" class="mask" />
  </transition>
  <transition name="slide">
    <div
      v-if="isVisible"
      class="queue"
      :style="{
        '--c-bg': 'var(--c-black)',
        '--c-fg': 'var(--c-white)',
        bottom: `${bottom}px`,
      }"
    >
      <div class="container">
        <transition-group name="queue--disabled" mode="out-in">
          <QueueMedia
            v-for="(media, index) in mediaList"
            :key="`media-row-${media.uid}`"
            :index="index"
            :media="media"
            :is-current="media === currentMedia"
          />
        </transition-group>
      </div>
    </div>
  </transition>
  <transition name="slide">
    <div
      v-if="isVisible"
      class="actions"
      :style="{
        '--c-bg': 'var(--c-black)',
        '--c-fg': 'var(--c-white)',
      }"
    >
      <div class="container">
        <ShuffleControl />
        <div class="button" v-text="'Clear queue'" @click="clearQueue" />
        <Circle
          :size="48"
          @click="close"
          background-color="rgb(var(--c-black))"
          hover-background-color="rgba(var(--c-white), 0.1)"
        >
          <IconCaret :size="48" direction="down" color="rgb(var(--c-white))" />
        </Circle>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

.mask {
  z-index: 19;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: rgba(var(--c-black), 0.8);
}

.queue {
  z-index: 20;
  position: fixed;
  width: 100%;
  min-height: 100px;
  //max-height: calc(100% - 148px);
  max-height: calc(100% - 72px);
  overflow-y: auto;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  overscroll-behavior: contain;
  &::-webkit-scrollbar {
    display: none;
  }
  .container {
    @include container.default;
    padding-top: 2rem;
    padding-bottom: 92px;
  }
}

.actions {
  z-index: 21;
  border-top: 1px solid rgba(var(--c-white), 0.25);
  .container {
    @include container.default;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    > div {
      margin-left: 0.5rem;
    }
  }
  //backdrop-filter: blur(8px);
  position: fixed;
  bottom: 72px;
  width: 100%;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  //background: rgba(var(--c-black), 0.9);
  background-image: linear-gradient(rgba(0, 0, 0, 0), rgba(var(--c-black), 0.9) 10%);
  //background: #00e8a7;
}

// NOTE: generalise button styling if also used at other place(s)
.button {
  cursor: pointer;
  height: 48px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  color: rgb(var(--c-white));
  //background: rgba(var(--c-white), 0.2);
  border: 1px solid rgba(var(--c-white), 0.2);
  transition: background-color 200ms;
  &:hover {
    border-color: transparent;
    background: rgba(var(--c-white), 0.1);
  }
}

// mask transition
.fade-enter-active,
.fade-leave-active {
  transition: opacity 200ms;
}
.fade-enter-from {
  opacity: 0;
}
.fade-leave-to {
  opacity: 0;
}

// queue panel transition
.slide-enter-active,
.slide-leave-active {
  transition: transform 200ms, opacity 200ms;
}
.slide-enter-from {
  transform: translate(0, 100%);
  opacity: 0;
}
.slide-leave-to {
  transform: translate(0, 100%);
}

// queue item list transition
.queue-enter-active,
.queue-leave-active {
  transition: opacity 300ms, transform 100ms;
}
//.queue-enter-from,
.queue-leave-to {
  opacity: 0;
  //transform: translateY(2rem);
}
</style>

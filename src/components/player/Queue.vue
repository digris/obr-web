<script lang="ts">
import {
  computed,
  defineComponent,
  onMounted,
} from 'vue';
import { useStore } from 'vuex';
import QueueMedia from '@/components/player/QueueMedia.vue';

export default defineComponent({
  components: {
    QueueMedia,
  },
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  emits: [
    'close',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const mediaList = computed(() => store.getters['queue/media']);
    const currentIndex = computed(() => store.getters['queue/currentIndex']);
    const currentMedia = computed(() => store.getters['queue/currentMedia']);
    const close = () => {
      emit('close');
    };

    onMounted(() => {
      document.addEventListener('keydown', (e) => {
        if (props.isVisible && e.code === 'KeyX') {
          close();
        }
      });
    });
    return {
      close,
      mediaList,
      currentIndex,
      currentMedia,
    };
  },
});
</script>
<template>
  <transition name="slide">
    <div
      v-if="isVisible"
      class="queue"
    >
      <div
        class="container"
      >
        <!--
        <div>
          ci: {{ currentIndex }}
        </div>
        <pre
          v-text="currentMedia"
        ></pre>
        -->
        <QueueMedia
          v-for="(media, index) in mediaList"
          :key="`media-row-${index}`"
          :media="media"
          :is-current="(media === currentMedia)"
        />
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

$player-height: 72px;

.container {
  @include container.default;
  padding: 2rem 0;
}

.queue {
  position: fixed;
  bottom: $player-height;
  width: 100%;
  min-height: 100px;
  max-height: 75%;
  overflow-y: auto;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  &::-webkit-scrollbar {
    display: none;
  }
}

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
</style>

<script lang="ts">
import {
  computed,
  defineComponent,
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
    const close = () => {
      emit('close');
    };
    return {
      close,
      mediaList,
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
      <QueueMedia
        v-for="(media, index) in mediaList"
        :key="`media-row-${index}`"
        :media="media"
      />
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

$player-height: 60px;

.container {
  @include container.default;
}

.queue {
  position: fixed;
  bottom: $player-height;
  width: 100%;
  min-height: 100px;
  max-height: 75%;
  overflow-y: auto;
  color: rgb(var(--c-black));;
  background: rgb(var(--c-white));
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

<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
  props: {
    isCurrent: {
      type: Boolean,
      default: true,
    },
    item: {
      type: Object,
      required: false,
      default: null,
    },
  },
  emits: [
    'play',
  ],
  setup(props, { emit }) {
    // eslint-disable-next-line arrow-body-style
    const ctaText = computed(() => {
      return (props.isCurrent) ? 'Listen' : 'Play';
    });
    const play = () => {
      emit('play');
    };
    return {
      ctaText,
      play,
    };
  },
});
</script>

<template>
  <div
    @click="play"
    class="play"
  >
    <div
      class="play__cta"
    >
      {{ ctaText }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
$size: 128px;
.play {
  display: flex;
  align-items: center;
  justify-content: center;
  width: $size;
  height: $size;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  border-radius: $size / 2;
  cursor: pointer;
  transition: color 100ms, background 100ms;
  &:hover {
    color: rgb(var(--c-black));
    background: rgb(var(--c-white));
  }
  &__cta {
    //text-transform: uppercase;
    font-size: 2rem;
  }
}
</style>

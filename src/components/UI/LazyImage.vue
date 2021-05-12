<script>
import { ref, watch } from 'vue';
// eslint-disable-next-line import/extensions
import Intersect from '@/components/utils/intersect.js';

// eslint-disable-next-line max-len
const PLACEHOLDER_SRC = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=';

export default {
  components: { Intersect },
  props: {
    src: {
      type: String,
      required: false,
      default: null,
    },
  },
  setup(props) {
    const isLoading = ref(false);
    const isLoaded = ref(false);
    const imageSrc = ref(PLACEHOLDER_SRC);

    const loadImage = async () => {
      isLoading.value = true;
      const img = new Image();
      img.src = props.src;
      img.addEventListener('load', () => {
        isLoading.value = false;
        isLoaded.value = true;
        imageSrc.value = props.src;
      }, true);
    };

    const onEnter = () => {
      if (!props.src) {
        return;
      }
      if (isLoading.value || isLoaded.value) {
        return;
      }
      loadImage();
    };

    watch(
      () => props.src,
      async () => {
        isLoading.value = false;
        isLoaded.value = false;
        imageSrc.value = PLACEHOLDER_SRC;

        loadImage();
      },
    );

    return {
      isLoading,
      isLoaded,
      imageSrc,
      onEnter,
    };
  },
};
</script>

<template>
  <Intersect
    @enter="onEnter"
  >
    <img
      :title="imageSrc"
      :src="imageSrc"
      :class="{'is-pending': !isLoaded, 'is-loading': isLoading}"
    />
  </Intersect>
</template>

<style lang="scss" scoped>
img {
  min-width: 100%;
  max-width: 100%;
  opacity: 1;
  filter: blur(0) brightness(0.95) grayscale(0.2);
  transition: filter 100ms, opacity 100ms;
  &.is-pending,
  &.is-loading {
    opacity: 0.5;
    filter: blur(2px);
  }
}
</style>

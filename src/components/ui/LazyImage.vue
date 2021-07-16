<script>
import { computed, ref, watch } from 'vue';
// eslint-disable-next-line import/extensions
import Intersect from '@/components/utils/intersect.js';
import { getImageColor, getImageSrc } from '@/utils/image';

// eslint-disable-next-line max-len
const PLACEHOLDER_SRC = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=';

export default {
  components: { Intersect },
  props: {
    image: {
      type: Object,
      required: false,
      default: null,
    },
  },
  setup(props) {
    const isLoading = ref(false);
    const isLoaded = ref(false);
    const size = ref(800);
    const imageSrc = ref(PLACEHOLDER_SRC);

    const color = computed(() => {
      return getImageColor(props.image);
    });

    const src = computed(() => {
      return getImageSrc(props.image, size.value);
    });

    const loadImage = async () => {
      isLoading.value = true;
      const img = new Image();
      img.src = src.value;
      img.addEventListener('load', () => {
        isLoading.value = false;
        isLoaded.value = true;
        imageSrc.value = src.value;
      }, true);
    };

    const onEnter = () => {
      if (!src.value) {
        return;
      }
      if (isLoading.value || isLoaded.value) {
        return;
      }
      loadImage();
    };

    const cssVars = computed(() => {
      if (!color.value) {
        return {};
      }
      const rgb = color.value.join(',');
      return {
        '--c-color': rgb,
      };
    });

    watch(
      () => src.value,
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
      cssVars,
      //
      src,
    };
  },
};
</script>

<template>
  <Intersect
    @enter="onEnter"
  >
    <img
      :alt="imageSrc"
      :src="imageSrc"
      :style="cssVars"
      :class="{'is-pending': !isLoaded, 'is-loading': isLoading}"
    />
  </Intersect>
</template>

<style lang="scss" scoped>
img {
  min-width: 100%;
  max-width: 100%;
  height: 100%;
  background: rgb(var(--c-color));
  opacity: 1;
  filter: brightness(0.95) grayscale(0.1);
  transition: opacity 100ms;
  image-rendering: pixelated;
  &.is-pending,
  &.is-loading {
    opacity: 0.9;
  }
}
</style>

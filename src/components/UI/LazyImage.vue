<script>
import { ref } from 'vue';
import Intersect from '@/components/utils/intersect';

// eslint-disable-next-line max-len
const PLACEHOLDER_SRC = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=';

export default {
  components: { Intersect },
  props: {
    src: {
      type: String,
      required: true,
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
      if (isLoading.value || isLoaded.value) {
        return;
      }
      loadImage();
    };

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
      :src="imageSrc"
      :class="{'is-pending': !isLoaded, 'is-loading': isLoading}"
    />
  </Intersect>
</template>

<style lang="scss" scoped>
img {
  min-width: 100%;
  max-width: 100%;
  filter: blur(0);
  opacity: 1;
  transition: filter 100ms, opacity 100ms;
  &.is-pending,
  &.is-loading {
    filter: blur(5px);
    opacity: 0.5;
  }
}
</style>

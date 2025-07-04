<script>
import { computed, ref, watch } from "vue";
import { useElementSize } from "@vueuse/core";

import Intersect from "@/components/utils/intersect.js";
import { getImageColor, getImageSrc } from "@/utils/image";

// eslint-disable-next-line max-len
const PLACEHOLDER_SRC =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";

export default {
  components: { Intersect },
  props: {
    image: {
      type: Object,
      required: false,
      default: null,
    },
    size: {
      type: Number,
      default: 800,
    },
    ratio: {
      type: Number,
      default: 1,
    },
    preload: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const imageEl = ref(null);
    const isLoading = ref(false);
    const isLoaded = ref(false);
    const imageSrc = ref(PLACEHOLDER_SRC);

    const { height: imageHeight, width: imageWidth } = useElementSize(imageEl);

    const calculatedSize = computed(() => {
      return Math.round(Math.max(imageHeight.value, imageWidth.value));
    });

    const color = computed(() => {
      return getImageColor(props.image);
    });

    const src = computed(() => {
      return getImageSrc(props.image, calculatedSize.value);
      // return getImageSrc(props.image, props.size);
    });

    const loadImage = async () => {
      isLoading.value = true;
      const img = new Image();
      img.src = src.value;
      img.addEventListener(
        "load",
        () => {
          isLoading.value = false;
          isLoaded.value = true;
          imageSrc.value = src.value;
        },
        true
      );
    };

    const onEnter = () => {
      if (!calculatedSize.value) {
        return;
      }
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
        return {
          "--c-color": "128 128 128",
        };
      }
      const rgb = color.value.join(" ");
      return {
        "--c-color": rgb,
      };
    });

    watch(
      () => src.value,
      async () => {
        isLoading.value = false;
        isLoaded.value = false;
        imageSrc.value = PLACEHOLDER_SRC;

        await loadImage();
      }
    );

    watch(
      calculatedSize,
      (val) => {
        if (props.preload && val > 0 && !isLoaded.value && !isLoading.value) {
          loadImage();
        }
      },
      { immediate: true }
    );

    return {
      imageEl,
      isLoading,
      isLoaded,
      imageSrc,
      onEnter,
      cssVars,
      //
      imageHeight,
      imageWidth,
      src,
    };
  },
};
</script>

<template>
  <Intersect @enter="onEnter">
    <div
      class="lazy-image"
      :style="{
        '--ratio': ratio,
      }"
    >
      <img
        alt="Image"
        ref="imageEl"
        :src="imageSrc"
        :style="cssVars"
        :class="{
          'is-pending': !isLoaded,
          'is-loading': isLoading,
        }"
        :fetchpriority="preload ? 'high' : undefined"
      />
      <div class="overlay">
        <slot name="default"></slot>
      </div>
    </div>
  </Intersect>
</template>

<style lang="scss" scoped>
.lazy-image {
  position: relative;
  max-width: 100%;
  aspect-ratio: var(--ratio);
  overflow: hidden;

  img {
    min-width: 100%;
    max-width: 100%;
    background: rgb(var(--c-color));
    opacity: 1;
    filter: var(--image-filter);
    transition: opacity 100ms;
    image-rendering: pixelated;
    aspect-ratio: var(--ratio);

    &.is-pending,
    &.is-loading {
      opacity: 0.9;
    }
  }

  .overlay {
    top: 0;
    position: absolute;
    width: 100%;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    aspect-ratio: var(--ratio);
  }
}
</style>

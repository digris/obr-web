<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import { debounce } from "lodash-es";

import IconFlash from "@/components/ui/icon/IconFlash.vue";
import IconHeart from "@/components/ui/icon/IconHeart.vue";
import { useIconSize } from "@/composables/icon";
import { useRating } from "@/composables/rating";

export default defineComponent({
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    autoload: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    iconScale: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: "--c-fg",
    },
    hideIfUnset: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    IconHeart,
    IconFlash,
  },
  setup(props) {
    const { iconSize } = useIconSize(props.iconScale);
    const { ratingByKey, loadRating, setRatingWithSource } = useRating();
    const rating = computed(() => ratingByKey(props.objKey));
    const isFlipped = ref(false);
    const flipIcon = async () => {
      isFlipped.value = true;
      return new Promise<void>((resolve) => {
        setTimeout(() => {
          isFlipped.value = false;
          resolve();
        }, 200);
      });
    };
    const rate = debounce(
      async (value: number) => {
        if (props.readonly) {
          return;
        }
        await flipIcon();
        await setRatingWithSource(props.objKey, value);
      },
      200,
      { leading: true, trailing: false }
    );
    onMounted(async () => {
      if (props.autoload && rating.value === undefined) {
        await loadRating(props.objKey);
      }
    });
    const style = computed(() => {
      const isEmpty = rating.value === null || rating.value === undefined;
      const opacity = props.hideIfUnset && isEmpty ? 0 : 1;
      return {
        height: `${iconSize.value}px`,
        width: `${iconSize.value}px`,
        opacity,
      };
    });
    return {
      rating,
      rate,
      style,
      iconSize,
      isFlipped,
    };
  },
});
</script>

<template>
  <div
    class="user-rating"
    :class="{
      'is-flipped': isFlipped,
    }"
    :style="style"
  >
    <IconHeart v-if="rating === 1" :scale="iconScale" :color-var="colorVar" @click="rate(null)" />
    <IconFlash
      v-else-if="rating === -1"
      :scale="iconScale"
      :color-var="colorVar"
      @click="rate(null)"
    />
    <IconHeart v-else :scale="iconScale" :outlined="true" :color-var="colorVar" @click="rate(1)" />
  </div>
</template>

<style lang="scss" scoped>
.user-rating {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 200ms ease-in-out, transform 200ms ease-in;

  &.is-flipped {
    transform: rotateY(89deg);
  }
}
</style>

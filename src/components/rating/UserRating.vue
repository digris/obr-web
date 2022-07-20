<script lang="ts">
import { computed, ref, defineComponent, onMounted } from "vue";
import { useStore } from "vuex";
import { debounce } from "lodash-es";
import { useIconSize } from "@/composables/icon";

import IconHeart from "@/components/ui/icon/IconHeart.vue";
import IconFlash from "@/components/ui/icon/IconFlash.vue";

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
    iconScale: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: "--c-black",
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
    const store = useStore();
    const { iconSize } = useIconSize(props.iconScale);
    const userRating = computed(() => {
      return store.getters["rating/ratingByKey"](props.objKey);
    });
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
        await flipIcon();
        const vote = {
          key: props.objKey,
          value,
        };
        await store.dispatch("rating/updateRating", vote);
      },
      200,
      { leading: true, trailing: false }
    );
    const style = computed(() => {
      return {
        height: `${iconSize.value}px`,
        width: `${iconSize.value}px`,
        opacity: props.hideIfUnset && userRating.value.value === null ? 0 : 1,
      };
    });
    onMounted(() => {
      if (props.autoload) {
        store.dispatch("rating/loadRating", props.objKey);
      }
    });
    return {
      userRating,
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
    v-if="userRating"
    class="user-rating"
    :class="{
      'is-flipped': isFlipped,
    }"
    :style="style"
  >
    <IconHeart
      v-if="userRating.value === 1"
      :scale="iconScale"
      @click="rate(null)"
      :color="`rgba(var(${colorVar}), 0.8)`"
    />
    <IconHeart
      v-if="userRating.value === null"
      :scale="iconScale"
      :outlined="true"
      @click="rate(1)"
      :color="`rgba(var(${colorVar}), 0.8)`"
    />
    <IconFlash
      v-if="userRating.value === -1"
      :scale="iconScale"
      :color="`rgba(var(${colorVar}), 0.8)`"
      @click="rate(null)"
    />
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

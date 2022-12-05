<script lang="ts">
import { computed, defineComponent, ref, onDeactivated } from "vue";
import { useElementHover } from "@vueuse/core";
import { getContrastColor } from "@/utils/color";
import { useObjKey } from "@/composables/obj";
import UserRating from "@/components/rating/UserRating.vue";

export default defineComponent({
  components: {
    UserRating,
  },
  props: {
    mood: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const el = ref();
    const { objKey } = useObjKey(props.mood);
    const link = `/discover/moods/${props.mood.uid}/`;
    const isHover = useElementHover(el);
    const cssVars = computed(() => {
      const bg = props.mood?.rgb ?? [128, 128, 128];
      const fg = getContrastColor(bg);
      return {
        "--c-bg": bg.join(","),
        "--c-fg": fg.join(","),
      };
    });
    onDeactivated(() => {
      isHover.value = false;
    });
    return {
      el,
      objKey,
      link,
      isHover,
      cssVars,
    };
  },
});
</script>
<template>
  <div ref="el" class="card card--mood" :style="cssVars">
    <router-link class="panel" :to="link">
      <div class="rating">
        <UserRating
          :obj-key="objKey"
          :readonly="true"
          :hide-if-unset="true"
          :color-var="isHover ? '--c-bg' : '--c-fg'"
        />
      </div>
      <div class="name" v-text="mood.name" />
      <div class="teaser" v-text="mood.teaser" />
    </router-link>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.card {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  color: rgb(var(--c-fg));
  background: rgb(var(--c-bg));
  transition: color 200ms, background 300ms;

  .panel {
    height: 100%;
    width: 100%;
    display: grid;
    color: rgb(var(--c-fg));

    .rating {
      position: absolute;
      height: calc(50%);
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .name {
      @include typo.large;

      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 1rem;
    }

    .teaser {
      @include typo.default;

      position: absolute;
      height: 50%;
      width: 100%;
      bottom: 1rem;
      align-items: flex-start;
      padding: 3rem 1rem 1rem;
      overflow-y: hidden;
      text-align: center;
    }
  }

  &:hover {
    color: rgb(var(--c-bg));
    background: rgb(var(--c-black));

    .panel {
      color: rgb(var(--c-gb));
    }
  }

  @include responsive.bp-medium {
    .panel {
      .rating {
        height: unset;
        width: unset;
        right: 0;
      }

      .teaser {
        display: none;
      }
    }
  }
}
</style>

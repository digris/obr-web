<script lang="ts">
import { computed, defineComponent, ref, onDeactivated, onActivated } from "vue";
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
    onActivated(() => {
      console.debug("Mood - onActivated");
    });
    onDeactivated(() => {
      console.debug("Mood - onDeactivated");
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
@use "@/style/abstracts/responsive";
@use "@/style/base/typo";
.card {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  color: rgb(var(--c-fg));
  background: rgb(var(--c-bg));
  transition: color 200ms, background 300ms;
  &:hover {
    color: rgb(var(--c-bg));
    background: rgb(var(--c-black));
    .panel {
      color: rgb(var(--c-gb));
    }
  }
  .panel {
    display: grid;
    width: 100%;
    height: 100%;
    color: rgb(var(--c-fg));
    .rating {
      position: absolute;
      width: 100%;
      //height: calc(50% - var(--t-fs-large) / 2);
      height: calc(50%);
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
      bottom: 1rem;
      //display: flex;
      align-items: flex-start;
      width: 100%;
      height: 50%;
      padding: 3rem 1rem 1rem;
      overflow-y: hidden;
      text-align: center;
    }
  }
  @include responsive.bp-medium {
    .panel {
      .rating {
        width: unset;
        height: unset;
        right: 0;
      }
      .teaser {
        display: none;
      }
    }
  }
}
</style>

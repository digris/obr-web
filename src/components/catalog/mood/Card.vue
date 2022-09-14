<script lang="ts">
import { computed, defineComponent } from "vue";
import { getContrastColor } from "@/utils/color";

export default defineComponent({
  props: {
    mood: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const link = `/discover/moods/${props.mood.uid}/`;
    const cssVars = computed(() => {
      const bg = props.mood?.rgb ?? [128, 128, 128];
      const fg = getContrastColor(bg);
      return {
        "--c-bg": bg.join(","),
        "--c-fg": fg.join(","),
      };
    });
    return {
      link,
      cssVars,
    };
  },
});
</script>
<template>
  <div class="card card--mood" :style="cssVars">
    <router-link class="panel" :to="link">
      <div class="name">
        {{ mood.name }}
      </div>
      <div class="teaser">
        {{ mood.teaser }}
      </div>
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
      @include responsive.bp-medium {
        display: none;
      }
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
}
</style>

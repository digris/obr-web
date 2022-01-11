<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    mood: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const link = `/discover/moods/${props.mood.uid}/`;
    return {
      link,
    };
  },
});
</script>
<template>
  <div
    class="card card--mood"
  >
    <router-link
      class="panel"
      :to="link"
    >
      <div
        class="name"
      >
        {{ mood.name }}
      </div>
      <div
        class="teaser"
      >
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
  color: rgb(var(--c-black));
  background: rgb(var(--c-gray-200));
  transition: color 200ms, background 300ms;
  &:hover {
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
  }
  .panel {
    display: grid;
    width: 100%;
    height: 100%;
    .name {
      @include typo.large;
      display: flex;
      align-items: flex-start;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 1rem;
    }
    .teaser {
      @include typo.default;
      @include responsive.bp-small {
        display: none;
      }
      position: absolute;
      bottom: 1rem;
      display: flex;
      align-items: flex-start;
      height: 50%;
      padding: 3rem 1rem 1rem;
      overflow-y: hidden;
      text-align: center;
    }
  }
}
</style>

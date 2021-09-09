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
    // const link = '/discover/tracks/?tags=D78E9E87&tags=83F07540';
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
@use "@/style/base/typo";
.card {
  position: relative;
  width: 100%;
  height: 0;
  padding-top: 100%;
  overflow: hidden;
  color: rgb(var(--c-black));
  background: rgb(var(--c-gray-200));
  transition: color 200ms, background 300ms;
  &:hover {
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
  }
  .panel {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
    height: 100%;
    //padding: 1rem;
    //text-align: center;
    text-transform: lowercase;
    .name {
      @include typo.large;
      display: flex;
      align-items: flex-start;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 1rem;
      transition: height 100ms;
    }
    .teaser {
      @include typo.default;
      position: absolute;
      bottom: 0;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      height: 50%;
      padding: 1rem;
      text-align: center;
      opacity: 0;
      transition: opacity 100ms;
    }
    &:hover {
      .teaser {
        opacity: 1;
      }
    }
  }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    mood: {
      type: Object,
      required: true,
    },
  },
  setup() {
    // const link = `/discover/moods/${props.mood.uid}/`;
    const link = '/discover/tracks/?tags=D78E9E87&tags=83F07540';
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
      {{ mood.name }}
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
  background: red;
  background: rgb(var(--c-gray-200));
  transition: color 200ms, background 300ms;
  &:hover {
    color: rgb(var(--c-white));
    background: rgb(var(--c-black));
  }
  .panel {
    @include typo.x-large;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    text-transform: lowercase;
  }
}
</style>

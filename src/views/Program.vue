<script lang="ts">
// NOTE: the naming here is kind of confusing and maybe should be changed.
// this view (views/Program.view) is used as top-level view bound to /program/
// the actual program data is handled by components/broadcast/program/Program.vue
import { defineComponent } from 'vue';
import Program from '@/components/broadcast/program/Program.vue';

export default defineComponent({
  components: {
    Program,
  },
});
</script>
<template>
  <div
    class="program-view"
  >
    <div
      class="title"
    >
      Heute
    </div>
    <div
      class="body"
    >
      <Program />
    </div>
    <div
      class="lookup"
    >
      (( Lookup ))
      <input
        type="date"
        value="2022-02-01"
      >
      <input
        type="time"
      >
    </div>
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
.program-view {
  display: flex;
  flex-direction: column;
  margin-bottom: 12rem;
}
.title {
  @include container.default;
  @include typo.x-large;
  @include typo.bold;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}
.body {
  flex-grow: 1;
  background: rgb(var(--white));
}
.lookup {
  display: none;
  height: 200px;
  background: darkorange;
}
</style>

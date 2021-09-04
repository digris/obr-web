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
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
.program-view {
  margin-bottom: 12rem;
}
.title {
  @include container.default;
  @include typo.x-large;
  @include typo.bold;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
  text-align: center;
}
.body {
  background: rgb(var(--white));
}
</style>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

export default defineComponent({
  setup() {
    const route = useRoute();
    const path = ref(route.path);
    watch(
      () => route.path,
      async (newPath) => {
        path.value = newPath;
      },
    );
    return {
      path,
    };
  },
});
</script>

<template>
  <div class="not-found">
    <div class="header">
      <div class="title">
        <h1>Page does not exist</h1>
      </div>
    </div>
    <div class="body">
      <p>{{ path }}</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/elements/detail-header";
.not-found {
  @include container.default;
  margin-bottom: 12rem;
}
.header {
  @include detail-header.default;
}
</style>

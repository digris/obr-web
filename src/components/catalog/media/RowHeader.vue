<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({});
</script>

<template>
  <div class="media-row-header">
    <div class="container">
      <div class="label" />
      <div class="label label--track">Track:</div>
      <div class="label">Kŭnstler*in/Album:</div>
      <div class="label">Dauer/Airtime:</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.media-row-header {
  background: rgb(var(--c-white));
  padding: 0.5rem 0;
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-columns: 96px 8fr 6fr 2fr 96px;
  .label {
    &--track {
      margin-left: -48px;
    }
  }
}
</style>

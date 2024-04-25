<script setup lang="ts">
import type { Section } from "@/typings/api";

defineProps<{
  section: Section;
}>();
</script>

<template>
  <div v-if="section.ctaUrl" class="cta">
    <a :href="section.ctaUrl" target="_blank" class="button">{{
      section?.ctaTitle ?? section.ctaUrl
    }}</a>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/button";

.cta {
  margin-top: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgb(var(--c-dark) / 20%);
  display: flex;
  align-items: center;
  justify-content: center;

  .button {
    @include button.default;

    width: 100%;
    cursor: pointer;

    @include responsive.bp-medium-up {
      max-width: 280px;
    }
  }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    title: {
      type: String,
      required: false,
      default: null,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
  },
});
</script>

<template>
  <section
    class="section"
    :class="{
      'is-outlined': outlined,
    }"
  >
    <div
      class="title"
      v-if="title"
      v-text="title"
    />
    <div
      class="panel"
    >
      <slot name="default" />
    </div>
  </section>
</template>

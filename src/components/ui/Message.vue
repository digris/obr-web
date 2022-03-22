<script lang="ts">
import { defineComponent } from "vue";

export enum MessageLevel {
  Info = "info",
  Warning = "warning",
  Success = "success",
}

export default defineComponent({
  props: {
    body: {
      type: String,
      required: true,
    },
    level: {
      type: String,
      default: MessageLevel.Info,
    },
  },
  setup(props) {
    console.debug(props);
  },
});
</script>

<template>
  <div class="message" :class="`message--${level}`">
    <div class="message__body" v-html="body" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.message {
  @include typo.bold;
  padding: 1rem;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  &--info {
    background: rgb(var(--c-info));
  }
  &--warning {
    background: rgb(var(--c-warning));
  }
  &--success {
    background: rgb(var(--c-success));
  }
}
</style>

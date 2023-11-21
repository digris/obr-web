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
  color: rgb(var(--c-light) / 100%);
  background: rgb(var(--c-dark) / 100%);

  &--info {
    background: rgb(var(--c-info) / 100%);
  }

  &--warning {
    background: rgb(var(--c-warning) / 100%);
  }

  &--success {
    background: rgb(var(--c-success) / 100%);
  }
}
</style>

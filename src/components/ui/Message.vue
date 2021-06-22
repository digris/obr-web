<script lang="ts">
import { defineComponent } from 'vue';

export enum MessageLevel {
  Info = 'info',
  Warning = 'warning',
  Success = 'success',
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
  <div
    class="message"
    :class="`message--${level}`"
  >
    <div
      class="message__body"
      v-html="body"
    />
  </div>
</template>

<style lang="scss" scoped>
.message {
  padding: 0.5rem 1rem 0.5rem calc(1rem - 4px);
  background: rgba(var(--c-black), 0.05);
  border-left: 4px solid rgb(var(--c-black));
  &--info {
    background: rgba(var(--c-info), 0.075);
    border-color: rgb(var(--c-info));
  }
  &--warning {
    background: rgba(var(--c-warning), 0.075);
    border-color: rgb(var(--c-warning));
  }
  &--success {
    background: rgba(var(--c-success), 0.075);
    border-color: rgb(var(--c-success));
  }
}
</style>

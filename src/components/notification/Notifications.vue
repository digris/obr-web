<script lang="ts">
import { defineComponent } from "vue";

import { useNotification } from "@/composables/notification";

import CloseButton from "./CloseButton.vue";

export default defineComponent({
  components: {
    CloseButton,
  },
  setup() {
    const { messages, setMessageSeen } = useNotification();
    return {
      messages,
      setMessageSeen,
    };
  },
});
</script>

<template>
  <div class="notifications">
    <div
      v-for="(message, index) in messages"
      :key="`message-${index}-${message.key}`"
      class="message"
      :class="`is-${message.level}`"
    >
      <div @click="setMessageSeen(message.key)" class="close">
        <CloseButton />
      </div>
      <div class="body" v-text="message.body" />
      <div v-if="message.action && message.action.label" class="action">
        <router-link :to="message.action.url" class="button">
          {{ message.action.label }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";

.notifications {
  top: 88px;
  position: fixed;
  right: 8px;
  z-index: 25;
}

.message {
  position: relative;
  min-width: 300px;
  max-width: 400px;
  min-height: 2.5rem;
  padding: 1rem;
  background: rgb(var(--c-live-fg-inverse));

  .close {
    top: 0;
    position: absolute;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding-top: 0.5rem;
    padding-right: 0.75rem;
    padding-left: 0.5rem;
  }

  .body {
    max-width: 270px;
    padding-top: 2px;
    padding-bottom: 0;
  }

  .action {
    padding-top: 1rem;

    .button {
      @include button.default(2rem);
    }
  }

  &.is-success {
    color: rgb(var(--c-success-fg));
    background: rgb(var(--c-success));
  }

  &.is-error {
    color: rgb(var(--c-error-fg));
    background: rgb(var(--c-error));
  }
}
</style>

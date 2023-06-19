<script lang="ts" setup>
import { useNotification } from "@/composables/notification";

import CloseButton from "./CloseButton.vue";

const { messages, setMessageSeen } = useNotification();
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
      <div v-if="message.action" class="action">
        <router-link :to="message.action.url" class="button" v-text="message.action.label" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/button";

.notifications {
  top: 88px;
  position: fixed;
  right: 8px;
  z-index: 125;

  @include responsive.bp-medium {
    top: calc(var(--sa-t) + 66px);
    right: 0;
    left: 0;
  }
}

.message {
  position: relative;
  min-width: 300px;
  max-width: 400px;
  padding: 1rem;
  background: rgb(var(--c-live-fg-inverse));
  display: grid;
  grid-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "body    close"
    "actions actions";

  .body {
    grid-area: body;
    display: flex;
    align-items: center;
  }

  .close {
    grid-area: close;
    display: flex;
    align-items: flex-start;
    justify-content: flex-end;
    cursor: pointer;
  }

  .action {
    grid-area: actions;
    margin-top: 1rem;

    .button {
      @include button.default(2rem);
    }
  }

  @include responsive.bp-medium {
    min-width: unset;
    max-width: unset;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-right: 0.5rem;

    .action {
      display: flex;
      justify-content: center;

      .button {
        min-width: 150px;
        max-width: 50%;
      }
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

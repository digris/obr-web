<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  setup() {
    const store = useStore();
    const messages = computed(() => store.getters['notification/messages']);
    const setSeen = (message: object) => {
      store.dispatch('notification/setMessageSeen', message);
    };
    return {
      messages,
      setSeen,
    };
  },
});
</script>

<template>
  <div
    class="notifications"
  >
    <div
      v-for="(message, index) in messages"
      :key="`message-${index}-${message.key}`"
      class="message"
      :class="`is-${message.level}`"
    >
      <div
        @click="setSeen(message)"
        class="close"
      >
        <span>-</span>
      </div>
      <div
        class="body"
        v-text="message.body"
      />
      <div
        v-if="message.action && message.action.label"
        class="action"
      >
        <router-link
          :to="message.action.url"
          class="button"
        >
          {{ message.action.label }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";
.notifications {
  position: fixed;
  top: 60px;
  right: 50px;
}

.message {
  position: relative;
  min-width: 300px;
  min-height: 3rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: rgb(var(--c-black));
  .close {
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
    cursor: pointer;
  }
  .body {
    padding-bottom: 1rem;
  }
  .action {
    .button {
      @include button.default(2rem);
    }
  }
  &.is-success {
    color: rgb(var(--c-black));
    background: rgb(var(--c-success));
  }
}
</style>

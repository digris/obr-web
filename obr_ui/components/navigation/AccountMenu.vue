<script lang="ts">
import { defineComponent } from "vue";

import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

export default defineComponent({
  setup() {
    const { user } = useAccount();
    const login = () => {
      const event = {
        intent: "login",
        next: window.location.pathname,
      };
      eventBus.emit("account:authenticate", event);
    };
    return {
      user,
      login,
    };
  },
});
</script>

<template>
  <div>
    <div class="account-menu" v-if="!user">
      <i18n-t
        tag="a"
        href="#"
        @click.prevent="login"
        class="menu-link"
        keypath="account.auth.login"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";

@mixin menu-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
  padding: 0 2rem;
  color: inherit;
  text-decoration: none;
  border-radius: 24px;
  transition: color, border 100ms 400ms, background-color 500ms;
  border: 1px solid rgb(var(--c-page-fg) / 25%);

  &:hover {
    @include live-color.bg-inverse(10%);

    transition: color, background-color 200ms;
  }
}

.account-menu {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: inherit;

  > a.menu-link {
    @include menu-button;
  }
}
</style>

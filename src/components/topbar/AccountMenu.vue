<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';

export default defineComponent({
  setup() {
    const store = useStore();
    const user = computed(() => store.getters['account/user']);
    const initials = computed(() => {
      if (!user.value) {
        return '?';
      }
      if (user.value.firstName) {
        return user.value.firstName.substr(0, 1).toUpperCase();
      }
      return user.value.email.substr(0, 1).toUpperCase();
    });
    const login = () => {
      const event = {
        intent: 'login',
        next: window.location.pathname,
      };
      eventBus.emit('account:authenticate', event);
    };
    return {
      user,
      initials,
      login,
    };
  },
});
</script>

<template>
  <div>
    <!--
    <div
      class="account-menu"
      v-if="user"
    >
      <router-link
        :to="{ name: 'accountSettings' }"
        v-slot="{ isActive }"
      >
        <CircleButton
          :size="(48)"
          :active="isActive"
        >
          {{ initials }}
        </CircleButton>
      </router-link>
    </div>
    -->
    <div
      class="account-menu"
      v-if="(!user)"
    >
      <a
        href="#"
        @click.prevent="login"
        class="menu-link"
      >
        Login
      </a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";
@mixin menu-link {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 0 2rem;
  color: inherit;
  text-decoration: none;
  transition: color, background-color 500ms;
  &:hover,
  &.router-link-active {
    color: #fff;
    background: black;
    transition: color, background-color 200ms;
  }
}
@mixin menu-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
  padding: 0 2rem;
  color: inherit;
  text-decoration: none;
  border-radius: 24px;
  transition: color, background-color 500ms;
  &:hover {
    @include live-color.bg-inverse(0.1);
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
  .submenu {
    @include live-color.bg(0.9);
    position: absolute;
    top: 72px;
    display: flex;
    flex-direction: column;
    > a {
      @include menu-link;
      height: 48px;
    }
  }
}
</style>

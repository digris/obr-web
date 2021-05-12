<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';

export default defineComponent({
  setup() {
    const router = useRouter();
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    const submenuVisible = ref(false);
    const login = () => {
      const event = {
        intent: 'login',
        next: window.location.pathname,
      };
      eventBus.emit('account:authenticate', event);
    };
    const logout = async () => {
      console.debug('trigger logout');
      try {
        await store.dispatch('account/logoutUser');
        await router.push({ name: 'home' });
      } catch (err) {
        console.debug('err', err);
      }
    };
    const showSubmenu = () => {
      submenuVisible.value = true;
    };
    const hideSubmenu = () => {
      submenuVisible.value = false;
    };
    return {
      currentUser,
      submenuVisible,
      login,
      logout,
      showSubmenu,
      hideSubmenu,
    };
  },
});
</script>

<template>
  <div>
    <div
      class="account-menu"
      v-if="currentUser"
      @mouseenter="showSubmenu"
      @mouseleave="hideSubmenu"
    >
      <!--
      <span>{{ currentUser.email }}</span>
      -->
      <router-link
        :to="{ name: 'accountSettings' }"
      >
        Account
      </router-link>
      <div
        v-if="submenuVisible"
        class="submenu"
      >
        <a
          href="#"
          @click.prevent="logout"
        >
          Logout
        </a>
      </div>
    </div>
    <div
      class="account-menu"
      v-else
    >
      <a
        href="#"
        @click.prevent="login"
      >
        Login
      </a>
      <!--
      <router-link
        :to="{ name: 'accountLogin' }"
      >
        Login
      </router-link>
      -->
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

.account-menu {
  height: 100%;
  color: inherit;
  > a {
    @include menu-link;
  }
  .submenu {
    @include live-color.bg(0.9);
    position: absolute;
    display: flex;
    flex-direction: column;
    > a {
      @include menu-link;
      height: 48px;
    }
  }
}
</style>

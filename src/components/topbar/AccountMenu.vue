<script lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  setup() {
    const router = useRouter();
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    const logout = async () => {
      console.debug('trigger logout');
      try {
        await store.dispatch('account/logoutUser');
        await router.push({ name: 'home' });
      } catch (err) {
        console.debug('err', err);
      }
    };
    return {
      currentUser,
      logout,
    };
  },
};
</script>

<template>
  <div>
    <div
      class="account-menu"
      v-if="currentUser"
    >
      <!--
      <span>{{ currentUser.email }}</span>
      -->
      <a
        href="#"
        @click.prevent="logout"
      >
        Logout
      </a>
    </div>
    <div
      class="account-menu"
      v-else
    >
      <router-link
        :to="{ name: 'accountLogin' }"
      >
        Login
      </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.account-menu {
  height: 100%;
  color: inherit;
  > a {
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
}
</style>

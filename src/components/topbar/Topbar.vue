<script lang="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';
import MainMenu from '@/components/topbar/MainMenu.vue';

export default {
  components: {
    MainMenu,
  },
  setup() {
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    return {
      currentUser,
    };
  },
};
</script>
<template>
  <div class="topbar">
    <div class="brand">
      open broadcast
    </div>
    <MainMenu/>
    <div class="menu menu--account">
      <div
        v-if="currentUser"
      >
        <router-link to="/account/">{{ currentUser.email }}</router-link>
      </div>
      <div
        v-else
      >
        <router-link to="/account/login/">Login</router-link>
      </div>
    </div>
    <div class="menu-toggle">
      +
    </div>
  </div>
</template>

<style lang="scss">
.topbar {
  position: sticky;
  top: 0;
  display: grid;
  grid-template-columns: 180px 1fr 120px 40px;
  height: 48px;
  background: rgba(var(--c-live-bg), 0.9);
  transition: background 3000ms;
  backdrop-filter: blur(2px);
  z-index: 2;
  .brand {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 1rem;
  }
  .menu {
    display: flex;
    align-items: center;
    &--main {
      justify-content: center;
    }
    &--account {
      justify-content: flex-end;
    }
  }
  .menu-toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0 1rem;
  }
  .menu {
    color: inherit;
    > a {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 2rem;
      height: 100%;
      color: inherit;
      text-decoration: none;
      transition: color, background-color 200ms;
      &:hover,
      &.router-link-active {
        color: #fff;
        background: black;
      }
    }
  }
}
</style>

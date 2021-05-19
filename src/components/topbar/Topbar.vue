<script lang="ts">
import MainMenu from '@/components/topbar/MainMenu.vue';
import AccountMenu from '@/components/topbar/AccountMenu.vue';

export default {
  components: {
    MainMenu,
    AccountMenu,
  },
};
</script>

<template>
  <div class="topbar">
    <div class="brand">
      <router-link
        to="/"
      >
        open broadcast
      </router-link>
    </div>
    <MainMenu
      class="menu menu--main"
    />
    <AccountMenu
      class="menu menu--account"
    />
    <div
      class="menu-toggle"
    >
      +
    </div>
  </div>
</template>

<style lang="scss" scoped>
.topbar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: grid;
  grid-template-columns: 180px 1fr 120px 40px;
  height: 48px;
  background: rgba(var(--c-live-bg), 0.9);
  backdrop-filter: blur(2px);
  transition: background 3000ms;
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
}
</style>

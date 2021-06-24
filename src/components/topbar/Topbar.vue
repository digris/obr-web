<script lang="ts">
import MainMenu from '@/components/topbar/MainMenu.vue';
import AccountMenu from '@/components/topbar/AccountMenu.vue';
import SubscriptionStatus from '@/components/topbar/SubscriptionStatus.vue';

export default {
  components: {
    MainMenu,
    AccountMenu,
    SubscriptionStatus,
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
    <SubscriptionStatus
      class="menu menu--subscription"
    />
    <AccountMenu
      class="menu menu--account"
    />
    <div
      class="menu-toggle"
    >
      <router-link
        :to="{ name: 'discoverPlaylists' }"
      >
        x
      </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
.topbar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: grid;
  grid-template-columns: 180px 1fr 40px 120px 40px;
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
    @include responsive.bp-small {
      display: none;
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

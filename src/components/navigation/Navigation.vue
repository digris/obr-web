<script lang="ts">
import { defineComponent } from "vue";
import eventBus from "@/eventBus";
import Logo from "@/components/ui/logo/Logo.vue";
import MainMenu from "@/components/navigation/MainMenu.vue";
import AccountMenu from "@/components/navigation/AccountMenu.vue";
import SubscriptionStatus from "@/components/navigation/SubscriptionStatus.vue";
import ToggleSearchButton from "@/components/navigation/ToggleSearchButton.vue";
import ToggleMenuButton from "@/components/navigation/ToggleMenuButton.vue";

export default defineComponent({
  components: {
    Logo,
    MainMenu,
    AccountMenu,
    SubscriptionStatus,
    ToggleSearchButton,
    ToggleMenuButton,
  },
  setup() {
    const showSideMenu = () => {
      eventBus.emit("side-menu:show");
    };
    const showGlobalSearch = () => {
      eventBus.emit("global-search:show");
    };
    return {
      showSideMenu,
      showGlobalSearch,
    };
  },
});
</script>

<template>
  <div class="topbar">
    <router-link class="brand" to="/">
      <Logo />
      <span>open broadcast</span>
    </router-link>
    <MainMenu class="menu menu--main" />
    <div class="subscription-account">
      <SubscriptionStatus class="menu menu--subscription" />
      <AccountMenu class="menu menu--account" />
    </div>
    <div class="search-toggle" @click.prevent="showGlobalSearch">
      <ToggleSearchButton />
    </div>
    <div class="menu-toggle" @click.prevent="showSideMenu">
      <ToggleMenuButton />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/base/live-color";
.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: 242px 1fr 170px 72px 48px;
  width: 100%;
  height: 78px;
  background: rgba(var(--c-page-bg), 0.6);
  border-bottom: 7px solid rgb(var(--c-page-fg));
  transition: background 1000ms;
  backdrop-filter: blur(24px);
  @include responsive.bp-small {
    height: 66px;
    grid-template-columns: 160px 1fr 48px 48px;
  }
  .brand {
    @include live-color.fg;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    transition: color, background-color 200ms;
    .logo {
      margin-right: 12px;
    }
    &:hover {
      &:not(&.router-link-exact-active) {
        background: rgba(var(--c-page-fg), 0.1);
      }
      transition: color, background-color 200ms;
    }
    @include responsive.bp-small {
      padding-left: 0.625rem;
      padding-right: 0.625rem;
      line-height: 1.25rem;
      .logo {
        width: 60px;
      }
    }
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
  .subscription-account {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    > div {
      &:not(:last-child) {
        margin-right: 0.25rem;
      }
    }
    .language-chooser {
      padding-right: 1rem;
      margin-top: -12px;
      @include responsive.bp-small {
        display: none;
      }
    }
  }
  .search-toggle,
  .menu-toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0 1rem;
    @include responsive.bp-small {
      padding-right: 0.625rem;
    }
  }
}
</style>

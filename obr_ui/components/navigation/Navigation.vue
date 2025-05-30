<script lang="ts" setup>
import AccountMenu from "@/components/navigation/AccountMenu.vue";
import MainMenu from "@/components/navigation/MainMenu.vue";
import SubscriptionStatus from "@/components/navigation/SubscriptionStatus.vue";
import ToggleMenuButton from "@/components/navigation/ToggleMenuButton.vue";
import ToggleSearchButton from "@/components/navigation/ToggleSearchButton.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconProgram from "@/components/ui/icon/IconProgram.vue";
import Logo from "@/components/ui/logo/Logo.vue";
import { useAnalytics } from "@/composables/analytics";
import { useDevice } from "@/composables/device";
import eventBus from "@/eventBus";

const { isSmallScreen } = useDevice();
const { logUIEvent } = useAnalytics();

const showSideMenu = () => {
  eventBus.emit("side-menu:show");
  logUIEvent("side-menu:show");
};
const showGlobalSearch = () => {
  eventBus.emit("global-search:show");
  logUIEvent("global-search:show");
};
</script>

<template>
  <div class="topbar-container">
    <div class="ios-bar" />
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
      <router-link v-if="isSmallScreen" class="program" :to="{ name: 'programRedirect' }">
        <CircleButton>
          <IconProgram color-var="--c-page-fg" />
        </CircleButton>
      </router-link>
      <div class="menu-toggle" @click.prevent="showSideMenu">
        <ToggleMenuButton />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/live-color";

.topbar-container {
  top: 0;
  position: sticky;
  padding-top: var(--sa-t);
  z-index: 20;
  background: rgb(var(--c-page-bg) / 50%);

  /* stylelint-disable-next-line property-no-vendor-prefix */
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  transition: background-color 600ms, color 100ms 1ms;
}

.topbar {
  top: var(--sa-t);
  position: sticky;
  height: 78px;
  width: 100%;
  z-index: 20;
  display: grid;
  grid-template-columns: 242px 1fr 146px 48px 48px;
  padding: 0 1.5rem 0 0;
  border-bottom: 7px solid rgb(var(--c-page-fg));

  // transition: background 10ms;
  transition: background-color 600ms, color 100ms 1ms;

  @include responsive.bp-medium {
    height: 66px;
    grid-template-columns: 172px 1fr 40px 40px 40px;
    padding: 0 0.625rem;
  }

  .brand {
    @include live-color.fg;

    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 1.5rem;
    padding-right: 1rem;
    transition: color, background-color 200ms;

    .logo {
      margin-right: 12px;
    }

    &:hover {
      &:not(&.router-link-exact-active) {
        background: rgb(var(--c-page-fg) / 10%);
      }

      transition: color, background-color 200ms;
    }

    @include responsive.bp-medium {
      line-height: 1.25rem;
      padding-left: 0;
      padding-right: 0;

      .logo {
        height: 40px;
        width: 40px;
        margin-right: 8px;
      }

      > span {
        margin-top: -6px;
        max-width: 100px;
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

    @include responsive.bp-medium {
      display: none;
    }
  }

  .subscription-account {
    display: flex;
    align-items: center;
    justify-content: flex-end;

    > div {
      &:not(:last-child) {
        margin-right: 0.75rem;
      }
    }
  }

  .program {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  .search-toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  .menu-toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
}
</style>

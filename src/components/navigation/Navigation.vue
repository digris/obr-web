<script lang="ts">
import { defineComponent } from "vue";

import AccountMenu from "@/components/navigation/AccountMenu.vue";
import MainMenu from "@/components/navigation/MainMenu.vue";
import SubscriptionStatus from "@/components/navigation/SubscriptionStatus.vue";
import ToggleMenuButton from "@/components/navigation/ToggleMenuButton.vue";
import ToggleSearchButton from "@/components/navigation/ToggleSearchButton.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconProgram from "@/components/ui/icon/IconProgram.vue";
import Logo from "@/components/ui/logo/Logo.vue";
import { useDevice } from "@/composables/device";
import eventBus from "@/eventBus";

export default defineComponent({
  components: {
    Logo,
    MainMenu,
    AccountMenu,
    SubscriptionStatus,
    ToggleSearchButton,
    ToggleMenuButton,
    CircleButton,
    IconProgram,
  },
  setup() {
    const { isMobile } = useDevice();
    const showSideMenu = () => {
      eventBus.emit("side-menu:show");
    };
    const showGlobalSearch = () => {
      eventBus.emit("global-search:show");
    };
    return {
      isMobile,
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
    <router-link v-if="isMobile" class="program" :to="{ name: 'programRedirect' }">
      <CircleButton>
        <IconProgram color-var="--c-page-fg" />
      </CircleButton>
    </router-link>
    <div class="menu-toggle" @click.prevent="showSideMenu">
      <ToggleMenuButton />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/live-color";

.topbar {
  top: 0;
  position: sticky;
  height: 78px;
  width: 100%;
  z-index: 20;
  display: grid;
  grid-template-columns: 242px 1fr 146px 48px 48px;
  padding: 0 1.5rem 0 0;
  background: rgb(var(--c-page-bg) 0.6);
  border-bottom: 7px solid rgb(var(--c-page-fg));
  transition: background 10ms;
  backdrop-filter: blur(24px);
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
        background: rgb(var(--c-page-fg) 0.1);
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

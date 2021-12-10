<script lang="ts">
import { defineComponent } from 'vue';
import eventBus from '@/eventBus';
import MainMenu from '@/components/topbar/MainMenu.vue';
import AccountMenu from '@/components/topbar/AccountMenu.vue';
import SubscriptionStatus from '@/components/topbar/SubscriptionStatus.vue';
import ToggleMenuButton from '@/components/topbar/ToggleMenuButton.vue';

export default defineComponent({
  components: {
    MainMenu,
    AccountMenu,
    SubscriptionStatus,
    ToggleMenuButton,
  },
  setup() {
    const showSideMenu = () => {
      eventBus.emit('side-menu:show');
    };
    return {
      showSideMenu,
    };
  },
});
</script>

<template>
  <div
    class="topbar"
  >
    <div
      class="brand"
    >
      <router-link
        to="/"
      >
        open broadcast
      </router-link>
    </div>
    <MainMenu
      class="menu menu--main"
    />
    <div
      class="subscription-and-account"
    >
      <SubscriptionStatus
        class="menu menu--subscription"
      />
      <AccountMenu
        class="menu menu--account"
      />
    </div>
    <div
      class="menu-toggle"
      @click.prevent="showSideMenu"
    >
      <ToggleMenuButton />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: 272px 1fr 200px 72px;
  width: 100%;
  height: 78px;
  background: rgba(var(--c-page-bg), 0.9);
  border-bottom: 7px solid rgb(var(--c-page-fg));
  //backdrop-filter: blur(2px);
  transition: background 1000ms;
  @include responsive.bp-small {
    grid-template-columns: 120px 1fr 120px;
  }
  .brand {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 1.5rem;
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
  .subscription-and-account {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    > div {
      &:not(:last-child) {
        margin-right: 1rem;
      }
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

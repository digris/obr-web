<script lang="ts">
import { computed, defineComponent } from "vue";
import { useWindowSize } from "@vueuse/core";

import { AppBridge } from "@/app-bridge/appBridge";
import AuthSidebar from "@/components/account/auth/AuthSidebar.vue";
import GeoblockNotice from "@/components/geolocation/GeoblockNotice.vue";
import CookieConsent from "@/components/legal/CookieConsent.vue";
import LegalLinks from "@/components/legal/LegalLinks.vue";
import GlobalSearch from "@/components/navigation/GlobalSearch.vue";
import Navigation from "@/components/navigation/Navigation.vue";
import SideMenu from "@/components/navigation/SideMenu.vue";
import Notifications from "@/components/notification/Notifications.vue";
import MobilePlayer from "@/components/player/mobile/Player.vue";
import Player from "@/components/player/Player.vue";
import Subscribe from "@/components/subscription/Subscribe.vue";
import ClaimVoucher from "@/components/subscription/voucher/Claim.vue";
import { useAccount } from "@/composables/account";
import { HlsPlayer } from "@/player/hlsPlayer";

declare global {
  interface Window {
    appBridge: AppBridge;
    hlsPlayer: HlsPlayer;
  }
}

export default defineComponent({
  name: "App",
  components: {
    Navigation,
    SideMenu,
    GlobalSearch,
    Notifications,
    AuthSidebar,
    Subscribe,
    GeoblockNotice,
    Player,
    ClaimVoucher,
    CookieConsent,
    LegalLinks,
  },
  setup() {
    const { loadUser } = useAccount();
    loadUser();

    window.appBridge = new AppBridge();
    window.hlsPlayer = HlsPlayer.getInstance();

    const { width: vpWidth } = useWindowSize();
    const playerComponent = computed(() => {
      return vpWidth.value < 500 ? MobilePlayer : Player;
    });
    return {
      playerComponent,
    };
  },
});
</script>

<template>
  <Navigation />
  <SideMenu />
  <GlobalSearch />
  <Notifications />
  <router-view v-slot="{ Component }">
    <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </router-view>
  <AuthSidebar />
  <Subscribe />
  <GeoblockNotice />
  <ClaimVoucher />
  <component :is="playerComponent" />
  <LegalLinks />
  <CookieConsent />
</template>

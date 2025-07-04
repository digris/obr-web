<script lang="ts">
import { defineComponent } from "vue";
import type { Emitter } from "mitt";

import { AppBridge } from "@/app-bridge/appBridge";
import AuthSidebar from "@/components/account/auth/AuthSidebar.vue";
import CompatibilityNotice from "@/components/browser-compatibility/CompatibilityNotice.vue";
import CtaPresenter from "@/components/cta/CtaPresenter.vue";
import DonateCta from "@/components/donation/DonateCta.vue";
import DonatePanel from "@/components/donation/DonatePanel.vue";
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
import { useDevice } from "@/composables/device";
import type { EventBusEvents } from "@/eventBus";
import { HlsPlayer } from "@/player/hlsPlayer";
import createMediaSessionHandler from "@/player/mediaSession";
import settings from "@/settings";
import createEventHandler from "@/stats/event";
import createHeartbeatHandler from "@/stats/heartbeat";
import createAccountHandler from "@/utils/account";
import createScheduleHandler from "@/utils/schedule";
import createUIStateHandler from "@/utils/ui";

import { init } from "./init";

declare global {
  interface Window {
    eventBus: Emitter<EventBusEvents>;
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
    MobilePlayer,
    DonateCta,
    DonatePanel,
    CtaPresenter,
    ClaimVoucher,
    CookieConsent,
    CompatibilityNotice,
    LegalLinks,
  },
  setup() {
    const { isApp, isWeb, isAndroid, isSmallScreen } = useDevice();

    window.hlsPlayer = HlsPlayer.getInstance();
    window.appBridge = AppBridge.getInstance();

    if (isApp) {
      console.debug("initialize: app-mode");
    }

    if (isWeb) {
      console.debug("initialize: web-mode");
      createEventHandler();
      createMediaSessionHandler();
      createScheduleHandler();
    }

    if (isAndroid && "serviceWorker" in navigator) {
      console.debug("initialize: android-mode");
      navigator.serviceWorker
        .register("/static/pwa/service-worker.js")
        .then(() => console.log("service worker: registered"))
        .catch((err) => console.log("service worker: registration failed:", err));
    }

    createAccountHandler();
    createUIStateHandler();
    createHeartbeatHandler();

    const { loadUser } = useAccount();
    loadUser();

    return {
      isSmallScreen,
      version: settings.VERSION,
    };
  },
  async mounted() {
    await init(this);
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
  <MobilePlayer v-if="isSmallScreen" />
  <Player v-else />
  <LegalLinks />
  <DonateCta />
  <DonatePanel />
  <CtaPresenter />
  <CookieConsent />
  <CompatibilityNotice />
  <div v-show="false" id="app-version" :data-version="version" v-text="version" />
</template>

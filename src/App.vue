<script lang="ts">
import { computed, defineComponent } from "vue";
import { useWindowSize } from "@vueuse/core";
import { AudioPlayer } from "@/player/audioPlayer";
import { useAccount } from "@/composables/account";
import Navigation from "@/components/navigation/Navigation.vue";
import SideMenu from "@/components/navigation/SideMenu.vue";
import GlobalSearch from "@/components/navigation/GlobalSearch.vue";
import AuthPanel from "@/components/account/AuthPanel.vue";
import Subscribe from "@/components/subscription/Subscribe.vue";
import Player from "@/components/player/Player.vue";
import MobilePlayer from "@/components/player/mobile/Player.vue";
import Notifications from "@/components/notification/Notifications.vue";
import ClaimVoucher from "@/components/subscription/voucher/Claim.vue";
import DebugPanel from "@/components/dev/DebugPanel.vue";

declare global {
  interface Window {
    audioPlayer: AudioPlayer;
  }
}

export default defineComponent({
  name: "App",
  components: {
    Navigation,
    SideMenu,
    GlobalSearch,
    Notifications,
    AuthPanel,
    Subscribe,
    Player,
    ClaimVoucher,
    DebugPanel,
  },
  setup() {
    const { loadUser } = useAccount();
    loadUser();

    window.audioPlayer = new AudioPlayer();

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
  <AuthPanel />
  <Subscribe />
  <ClaimVoucher />
  <component :is="playerComponent" />
  <DebugPanel />
</template>

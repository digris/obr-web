<script lang="ts">
import { computed, defineComponent } from "vue";
import { useStore } from "vuex";
import { useWindowSize } from "@vueuse/core";
import { AudioPlayer } from "@/player/audioPlayer";
import { Queue } from "@/player/queue";
import Navigation from "@/components/navigation/Navigation.vue";
import SideMenu from "@/components/navigation/SideMenu.vue";
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
    queue: Queue;
  }
}

export default defineComponent({
  name: "App",
  components: {
    Navigation,
    SideMenu,
    Notifications,
    AuthPanel,
    Subscribe,
    Player,
    ClaimVoucher,
    DebugPanel,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters["account/user"]);

    window.audioPlayer = new AudioPlayer();
    // @ts-ignore
    window.queue = new Queue();

    store.dispatch("account/getUser");
    const { width: vpWidth } = useWindowSize();
    const playerComponent = computed(() => {
      return vpWidth.value < 500 ? MobilePlayer : Player;
    });
    return {
      user,
      playerComponent,
    };
  },
});
</script>

<template>
  <Navigation />
  <SideMenu />
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

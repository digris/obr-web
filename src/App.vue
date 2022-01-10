<script>
import { AudioPlayer } from '@/player/audioPlayer';
import queue from '@/player/queue';
import Topbar from '@/components/topbar/Topbar.vue';
import SideMenu from '@/components/topbar/SideMenu.vue';
import AuthPanel from '@/components/account/AuthPanel.vue';
import Subscribe from '@/components/subscription/Subscribe.vue';
import Player from '@/components/player/Player.vue';
import Notifications from '@/components/notification/Notifications.vue';
import ClaimVoucher from '@/components/subscription/voucher/Claim.vue';
// import ColorChooser from '@/components/colors/ColorChooser.vue';

export default {
  components: {
    Topbar,
    SideMenu,
    Notifications,
    AuthPanel,
    Subscribe,
    Player,
    ClaimVoucher,
  },
  created() {
    this.$store.dispatch('account/getUser');
    this.audioPlayer = new AudioPlayer();
    this.queue = queue;
  },
  computed: {
    user() {
      return this.$store.getters['account/user'];
    },
  },
};
</script>

<template>
  <Topbar />
  <SideMenu />
  <Notifications />
  <router-view
    v-slot="{ Component }"
  >
    <keep-alive>
      <component
        :is="Component"
      />
    </keep-alive>
  </router-view>
  <AuthPanel />
  <Subscribe />
  <ClaimVoucher />
  <Player />
</template>

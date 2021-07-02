<script>
import { AudioPlayer } from '@/player/audioPlayer';
import { Queue } from '@/player/queue';
import Topbar from '@/components/topbar/Topbar.vue';
import AuthPanel from '@/components/account/AuthPanel.vue';
import Subscribe from '@/components/subscription/Subscribe.vue';
import Player from '@/components/player/Player.vue';
import Notifications from '@/components/notification/Notifications.vue';

export default {
  components: {
    Topbar,
    Notifications,
    AuthPanel,
    Subscribe,
    Player,
  },
  created() {
    this.$store.dispatch('account/getUser');
    this.audioPlayer = new AudioPlayer();
    this.queue = new Queue();
  },
  computed: {
    currentUser() {
      return this.$store.getters['account/currentUser'];
    },
  },
};
</script>

<template>
  <Topbar />
  <Notifications />
  <router-view v-slot="{ Component }">
    <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </router-view>
  <AuthPanel />
  <Subscribe />
  <Player />
</template>

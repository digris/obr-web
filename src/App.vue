<script>
import { AudioPlayer } from '@/player/audioPlayer';
import Topbar from '@/components/topbar/Topbar.vue';
import AuthPanel from '@/components/account/AuthPanel.vue';
import Subscribe from '@/components/subscription/Subscribe.vue';
import Player from '@/components/player/Player.vue';
import ColorChooser from '@/components/colors/ColorChooser.vue';

export default {
  components: {
    Topbar,
    AuthPanel,
    Subscribe,
    Player,
    ColorChooser,
  },
  created() {
    this.$store.dispatch('account/getUser');
    this.audioPlayer = new AudioPlayer();
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
  <router-view v-slot="{ Component }">
    <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </router-view>
  <ColorChooser />
  <AuthPanel />
  <Subscribe />
  <Player />
</template>

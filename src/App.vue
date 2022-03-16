<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import { useWindowSize } from '@vueuse/core';
import { AudioPlayer } from '@/player/audioPlayer';

import queue from '@/player/queue';
import Navigation from '@/components/navigation/Navigation.vue';
import SideMenu from '@/components/navigation/SideMenu.vue';
import AuthPanel from '@/components/account/AuthPanel.vue';
import Subscribe from '@/components/subscription/Subscribe.vue';
import Player from '@/components/player/Player.vue';
import MobilePlayer from '@/components/player/mobile/Player.vue';
import Notifications from '@/components/notification/Notifications.vue';
import ClaimVoucher from '@/components/subscription/voucher/Claim.vue';

export default defineComponent({
  name: 'App',
  components: {
    Navigation,
    SideMenu,
    Notifications,
    AuthPanel,
    Subscribe,
    Player,
    ClaimVoucher,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters['account/user']);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const audioPlayer = new AudioPlayer();
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const playerQueue = queue;
    store.dispatch('account/getUser');
    const {
      width: vpWidth,
    } = useWindowSize();
    const playerComponent = computed(() => {
      return (vpWidth.value < 500) ? MobilePlayer : Player;
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
  <component
    :is="playerComponent"
  />
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import { AudioPlayer } from '@/player/audioPlayer';

import queue from '@/player/queue';
import Topbar from '@/components/topbar/Topbar.vue';
import SideMenu from '@/components/topbar/SideMenu.vue';
import AuthPanel from '@/components/account/AuthPanel.vue';
import Subscribe from '@/components/subscription/Subscribe.vue';
import Player from '@/components/player/Player.vue';
import MobilePlayer from '@/components/player/mobile/Player.vue';
import Notifications from '@/components/notification/Notifications.vue';
import ClaimVoucher from '@/components/subscription/voucher/Claim.vue';

export default defineComponent({
  name: 'App',
  components: {
    Topbar,
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
    const viewport = computed(() => store.getters['ui/viewport']);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const audioPlayer = new AudioPlayer();
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const playerQueue = queue;
    store.dispatch('account/getUser');
    const playerComponent = computed(() => {
      return (viewport.value.width < 500) ? MobilePlayer : Player;
    });
    return {
      user,
      playerComponent,
    };
  },
});
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
  <component
    :is="playerComponent"
  />
</template>

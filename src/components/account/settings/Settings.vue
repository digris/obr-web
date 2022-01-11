<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import Subscription from '@/components/account/settings/Subscription.vue';
import Email from '@/components/account/settings/Email.vue';
import Password from '@/components/account/settings/Password.vue';
import Personal from '@/components/account/settings/Personal.vue';
import Address from '@/components/account/settings/Address.vue';
import Social from '@/components/account/settings/Social.vue';
// import Debug from '@/components/dev/Debug.vue';

export default defineComponent({
  components: {
    Subscription,
    Email,
    Password,
    Personal,
    Address,
    Social,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters['account/user']);
    const subscription = computed(() => store.getters['account/subscription']);
    const settings = computed(() => store.getters['account/settings']);
    const address = computed(() => store.getters['account/address']);
    const socialNext = window.location.pathname;
    const reloadUser = async () => {
      await store.dispatch('account/getUser');
    };
    return {
      user,
      subscription,
      settings,
      address,
      socialNext,
      reloadUser,
    };
  },
});
</script>

<template>
  <Subscription />
  <Email
    v-if="user"
    :user="user"
    @updated="reloadUser"
  />
  <Password />
  <Personal
    :user="user"
    @updated="reloadUser"
  />
  <Address
    :address="address"
    @updated="reloadUser"
  />
  <Social
    :next="socialNext"
  />
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import { useStore } from "vuex";

import SocialLogin from "@/components/account/SocialLogin.vue";
import Section from "@/components/account/settings/Section.vue";
import CurrentSubscription from "@/components/subscription/CurrentSubscription.vue";
import Password from "@/components/account/settings/Password.vue";
import Email from "@/components/account/settings/Email.vue";
import Personal from "@/components/account/settings/Personal.vue";
import Address from "@/components/account/settings/Address.vue";
// import Debug from '@/components/dev/Debug.vue';

export default defineComponent({
  components: {
    Section,
    SocialLogin,
    CurrentSubscription,
    Email,
    Password,
    Personal,
    Address,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters["account/user"]);
    const subscription = computed(() => store.getters["account/subscription"]);
    const settings = computed(() => store.getters["account/settings"]);
    const address = computed(() => store.getters["account/address"]);
    const socialNext = window.location.pathname;
    const reloadUser = async () => {
      await store.dispatch("account/getUser");
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
  <Section v-if="user" title="Guthaben für kostenpflichtige Inhalte">
    <CurrentSubscription />
  </Section>
  <Email v-if="user" :user="user" @updated="reloadUser" />
  <Password />
  <Personal :user="user" @updated="reloadUser" />
  <Address :address="address" @updated="reloadUser" />
  <Section v-if="user" title="Verbundene Accounts" :outlined="false">
    <SocialLogin :next="socialNext" />
  </Section>
</template>

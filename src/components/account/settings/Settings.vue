<script lang="ts">
import { computed, defineComponent } from "vue";
import { useStore } from "vuex";

import Section from "@/components/account/settings/Section.vue";
import CurrentSubscription from "@/components/subscription/CurrentSubscription.vue";
import Stream from "@/components/account/settings/Stream.vue";
import Email from "@/components/account/settings/Email.vue";
import Password from "@/components/account/settings/Password.vue";
import Personal from "@/components/account/settings/Personal.vue";
import Address from "@/components/account/settings/Address.vue";
import Social from "@/components/account/settings/Social.vue";
import Support from "@/components/account/settings/Support.vue";

export default defineComponent({
  components: {
    Section,
    CurrentSubscription,
    Stream,
    Email,
    Password,
    Personal,
    Address,
    Social,
    Support,
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
  <div v-if="user">
    <Section
      v-if="user"
      title="Guthaben für kostenpflichtige Inhalte"
      @edit="
        {
        }
      "
    >
      <CurrentSubscription />
    </Section>
    <Stream />
    <Email v-if="user" :user="user" @updated="reloadUser" />
    <Password />
    <Personal :user="user" @updated="reloadUser" />
    <Address :address="address" @updated="reloadUser" />
    <Social />
    <Support :user="user" />
  </div>
</template>

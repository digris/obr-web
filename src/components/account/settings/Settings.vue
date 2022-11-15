<script lang="ts">
import { defineComponent } from "vue";
import { useAccount } from "@/composables/account";
import { useDevice } from "@/composables/device";

import Section from "@/components/account/settings/Section.vue";
import CurrentSubscription from "@/components/subscription/CurrentSubscription.vue";
import Stream from "@/components/account/settings/Stream.vue";
import Email from "@/components/account/settings/Email.vue";
import Password from "@/components/account/settings/Password.vue";
import Personal from "@/components/account/settings/Personal.vue";
import Address from "@/components/account/settings/Address.vue";
import Social from "@/components/account/settings/Social.vue";
// import Support from "@/components/account/settings/Support.vue";
import QRCodeLogin from "@/components/account/qrcode/QRCodeLogin.vue";

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
    // Support,
    QRCodeLogin,
  },
  setup() {
    const { user, subscription, settings, address, loadUser } = useAccount();
    const { isDesktop } = useDevice();
    const socialNext = window.location.pathname;
    return {
      user,
      subscription,
      settings,
      address,
      socialNext,
      loadUser,
      isDesktop,
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
    <Email v-if="user" :user="user" @updated="loadUser" />
    <Password />
    <Personal :user="user" @updated="loadUser" />
    <Address :address="address" @updated="loadUser" />
    <Social />
    <!--
    <Support :user="user" />
    -->
    <QRCodeLogin v-if="isDesktop" :user="user" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import QRCodeLogin from "@/components/account/qrcode/QRCodeLogin.vue";
import Address from "@/components/account/settings/Address.vue";
import Email from "@/components/account/settings/Email.vue";
import Newsletter from "@/components/account/settings/Newsletter.vue";
import Password from "@/components/account/settings/Password.vue";
import Personal from "@/components/account/settings/Personal.vue";
import Section from "@/components/account/settings/Section.vue";
import Social from "@/components/account/settings/Social.vue";
import Stream from "@/components/account/settings/Stream.vue";
import CurrentSubscription from "@/components/subscription/CurrentSubscription.vue";
import { useAccount } from "@/composables/account";
import { useDevice } from "@/composables/device";
import Page from "@/layouts/Page.vue";

export default defineComponent({
  components: {
    Section,
    Page,
    CurrentSubscription,
    Stream,
    Email,
    Password,
    Personal,
    Address,
    Newsletter,
    Social,
    QRCodeLogin,
  },
  setup() {
    const { t } = useI18n();
    const { isApp, isDesktop } = useDevice();
    const { user, subscription, settings, address, loadUser } = useAccount();
    const socialNext = window.location.pathname;
    return {
      t,
      isApp,
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
  <Page v-if="user" :title="t('account.title')">
    <Section
      :readonly="isApp"
      v-if="user"
      class="subscription"
      :title="t('account.settings.subscription.title')"
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
    <Newsletter />
    <Social next="/account/settings/" />
    <QRCodeLogin v-if="isDesktop" :user="user" />
  </Page>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

section {
  &:first-child {
    margin-top: 0;
  }

  &.subscription {
    @include typo.large;
  }
}
</style>

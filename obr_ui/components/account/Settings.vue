<script lang="ts">
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import QRCodeLogin from "@/components/account/qrcode/QRCodeLogin.vue";
import Address from "@/components/account/settings/Address.vue";
import Donations from "@/components/account/settings/Donations.vue";
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
import { useSettings } from "@/composables/settings";
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
    Donations,
    QRCodeLogin,
  },
  setup() {
    const { t } = useI18n();
    const { isDesktop } = useDevice();
    const { user, subscription, settings, address, loadUser } = useAccount();
    const { userSettings } = useSettings();
    const testingEnabled = computed(() => userSettings.value?.testingEnabled);
    const socialNext = window.location.pathname;
    return {
      t,
      user,
      testingEnabled,
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
    <Donations v-if="user && testingEnabled" :donations="user.donations" />
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

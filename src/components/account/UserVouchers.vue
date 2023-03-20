<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import QRCodeApp from "@/components/account/qrcode/QRCodeApp.vue";
import UserVoucher from "@/components/account/voucher/UserVoucher.vue";
import { useSubscription } from "@/composables/subscription";
import Page from "@/layouts/Page.vue";

export default defineComponent({
  components: {
    Page,
    UserVoucher,
    QRCodeApp,
  },
  setup() {
    const { t } = useI18n();
    const { userVouchers } = useSubscription();
    return {
      t,
      userVouchers,
    };
  },
});
</script>

<template>
  <Page :title="t('menu.userVouchers')">
    <template #lead>
      <p>Spread the sound!</p>
    </template>
    <div class="cta">
      <p>Share the love with your friends and invite them to join!</p>
      <p>Simply let them scan the "iOS App install" QR code to install the app.</p>
      <p>
        Once they have the app, they can scan one of your "Voucher" QR codes to gain unlimited
        access.
      </p>
    </div>
    <section class="app">
      <h3>iOS App install</h3>
      <p>Let's scan the QR-code to install the app</p>
      <div class="qr-code-container">
        <QRCodeApp />
      </div>
    </section>
    <section class="vouchers">
      <h3>Vouchers</h3>
      <UserVoucher
        class="voucher"
        v-for="voucher in userVouchers"
        :key="`voucher-${voucher.uid}`"
        :voucher="voucher"
      />
    </section>
  </Page>
</template>

<style lang="scss" scoped>
.cta {
  > p {
    margin-bottom: 0.5rem;
  }
}

.vouchers {
  margin-top: 2rem;

  > h3 {
    margin-bottom: 1rem;
  }

  .voucher {
    margin-bottom: 2rem;
  }
}

.app {
  margin: 2rem 0 1rem;

  .qr-code-container {
    margin: 1rem 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>

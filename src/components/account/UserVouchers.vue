<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import UserVoucher from "@/components/account/voucher/UserVoucher.vue";
import { useSubscription } from "@/composables/subscription";
import Page from "@/layouts/Page.vue";

export default defineComponent({
  components: {
    Page,
    UserVoucher,
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
    <div>
      <p>
        Aliquam dignissim elementum aliquet. Mauris in urna ullamcorper, consequat libero sit amet,
        amet, mollis massa. Sed lobortis dignissim nisi id lacinia. In in hendrerit libero. In In
        sapien dui, varius sit amet turpis vitae, sodales varius enim.
      </p>
    </div>
    <section class="vouchers">
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
.vouchers {
  margin-top: 2rem;

  .voucher {
    margin-bottom: 2rem;
  }
}
</style>

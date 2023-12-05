<script lang="ts" setup>
import { useI18n } from "vue-i18n";

import { useDevice } from "@/composables/device";
const { t } = useI18n();
const { isDesktop } = useDevice();
const faqUrl = "/faq/#42C745E4";
</script>

<template>
  <div class="availability">
    <i18n-t keypath="account.legal.availability.note" tag="p">
      <sup v-show="isDesktop">*</sup>
      <router-link :to="faqUrl" v-text="t('account.legal.availability.faq')" />
    </i18n-t>
  </div>
</template>

<style lang="scss" scoped>
.availability {
  white-space: pre-line;

  a {
    text-decoration: underline;
  }
}
</style>

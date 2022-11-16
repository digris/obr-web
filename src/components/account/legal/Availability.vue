<script lang="ts" setup>
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const faqUrl = "/faq/";
</script>

<template>
  <div class="availability">
    <i18n-t keypath="account.legal.availability.note" tag="p">
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

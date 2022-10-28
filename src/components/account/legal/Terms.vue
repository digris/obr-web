<script lang="ts" setup>
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const tosUrl = "/legal/terms/";
const ppUrl = "/legal/terms/";
</script>

<template>
  <div class="terms">
    <i18n-t keypath="account.legal.terms.term" tag="p">
      <a :href="tosUrl" target="_blank" v-text="t('account.legal.terms.tos')" />
      <a :href="ppUrl" target="_blank" v-text="t('account.legal.terms.pp')" />
    </i18n-t>
  </div>
</template>

<style lang="scss" scoped>
//@use "@/style/base/typo";
.terms {
  //@include typo.small;
  a {
    text-decoration: underline;
  }
}
</style>

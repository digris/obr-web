<template>
  <div class="service">
    <i18n-t class="title" keypath="account.serviceInfoAside.title" tag="p" />
    <ul>
      <i18n-t keypath="account.serviceInfoAside.bullet1" tag="li" />
      <i18n-t keypath="account.serviceInfoAside.bullet2" tag="li" />
      <i18n-t keypath="account.serviceInfoAside.bullet3" tag="li"><sup>*</sup></i18n-t>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.service {
  color: rgb(var(--c-white));

  .title {
    @include typo.x-large;
    @include typo.bold;
  }

  > ul {
    margin-top: 1rem;
    line-height: 2;
    list-style-position: inside;
  }
}
</style>
<script setup lang="ts"></script>

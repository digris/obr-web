<template>
  <div class="account">
    <div class="header">
      <div class="title" v-text="$t('ACCOUNT.ACCOUNT')" />
    </div>
    <div class="body">
      <router-view></router-view>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/base/typo";
.account {
  @include container.small;
  margin-bottom: 12rem;
}
.header {
  @include typo.x-large;
  margin: 2rem 0 2rem;
}
</style>

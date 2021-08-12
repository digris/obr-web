<template>
  <div class="account">
    <div class="header">
      <div class="title">
        Konto
      </div>
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
  @include typo.large;
  margin: 2rem 0 4rem;
}
</style>

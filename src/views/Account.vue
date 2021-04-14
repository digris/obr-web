<template>
  <div class="account">
    <div class="header">
      <div class="title">
        <h1>Account</h1>
      </div>
    </div>
    <div class="body">
      <router-view></router-view>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/elements/detail-header";
.account {
  @include container.default;
  margin-bottom: 12rem;
}
.header {
  @include detail-header.default;
}
</style>

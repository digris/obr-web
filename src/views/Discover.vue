<template>
  <div class="discover">
    <div class="list-header">
      <div class="title">
        <h1>Discover</h1>
      </div>
    </div>
    <div class="list-menu">
      <div class="menu menu--primary">
        <router-link
          :to="{ name: 'discover' }"
        >
          Home
        </router-link>
        <router-link
          :to="{ name: 'discoverArtists' }"
        >
          Artists
        </router-link>
        <router-link
          :to="{ name: 'discoverMedia' }"
        >
          Tracks
        </router-link>
      </div>
    </div>
    <div class="list-body">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";
@use "@/style/elements/list-header";
@use "@/style/elements/list-menu";
.discover {
  @include container.default;
  margin-bottom: 12rem;
}
.list-header {
  @include list-header.default;
}
.list-menu {
  @include list-menu.default;
}
</style>

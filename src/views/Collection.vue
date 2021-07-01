<template>
  <div class="collection">
    <div class="list-header">
      <div class="title">
        <h1>My Likes</h1>
      </div>
    </div>
    <!--
    <div class="list-menu">
      <div class="menu menu--primary">
        <router-link
          :to="{ name: 'collectionMedia' }"
        >
          Tracks
        </router-link>
        <router-link
          :to="{ name: 'collectionArtists' }"
        >
          Artists
        </router-link>
      </div>
    </div>
    -->
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
@use "@/style/elements/container";
@use "@/style/elements/list-header";
@use "@/style/elements/list-menu";
.collection {
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

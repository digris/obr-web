<template>
  <div
    class="discover"
  >
    <div
      class="title"
    >
      Discover
    </div>
    <div
      class="list-menu"
    >
      <div
        class="menu menu--primary"
      >
        <router-link
          :to="{ name: 'discoverMoods' }"
        >
          Stimmung
        </router-link>
        <router-link
          :to="{ name: 'discoverMedia' }"
        >
          Tracks
        </router-link>
        <router-link
          :to="{ name: 'discoverArtists' }"
        >
          Künstler*innen
        </router-link>
        <router-link
          :to="{ name: 'discoverPlaylists' }"
        >
          Shows
        </router-link>
      </div>
      <div
        class="menu menu--secondary"
      >
        <router-view
          name="filterbar"
        />
      </div>
    </div>
    <div
      class="list-body"
    >
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/list-menu";
.discover {
  //@include container.default;
  margin-bottom: 12rem;
}
.title {
  @include container.default;
  @include typo.x-large;
  @include typo.bold;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
  text-align: center;
}
.list-menu {
  @include container.default;
  @include list-menu.default;
}
</style>

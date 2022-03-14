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
          v-text="`Stimmung`"
        />
        <router-link
          :to="{ name: 'discoverMedia' }"
          v-text="`Tracks`"
        />
        <router-link
          :to="{ name: 'discoverPlaylists' }"
          v-text="`Shows`"
        />
        <router-link
          :to="{ name: 'discoverArtists' }"
          v-text="`Künstler*innen`"
        />
        <router-link
          :to="{ name: 'discoverEditors' }"
          v-text="`Editor*innen`"
        />
      </div>
      <div
        class="menu menu--secondary"
      >
        <router-view
          name="searchbar"
        />
      </div>
    </div>
    <div
      class="list-body"
    >
      <router-view
        v-slot="{ Component }"
      >
        <keep-alive>
          <component
            :is="Component"
          />
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
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
}
.list-menu {
  @include container.default;
  @include list-menu.default;
}
</style>

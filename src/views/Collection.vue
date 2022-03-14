<template>
  <div
    class="collection"
  >
    <div
      class="title"
    >
      Favoriten
    </div>
    <div
      class="list-menu"
    >
      <div
        class="menu menu--primary"
      >
        <router-link
          :to="{ name: 'collectionMedia' }"
        >
          Tracks
        </router-link>
        <router-link
          :to="{ name: 'collectionPlaylists' }"
        >
          Shows
        </router-link>
        <router-link
          :to="{ name: 'collectionArtists' }"
        >
          Künstler*innen
        </router-link>
      </div>
      <div
        class="menu menu--secondary"
      >
        <router-view
          name="searchbar"
        />
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
.collection {
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

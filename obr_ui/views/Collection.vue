<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

export default defineComponent({
  setup() {
    const { t } = useI18n();
    return {
      t,
    };
  },
});
</script>

<template>
  <div class="collection">
    <div class="title" v-text="t('menu.collection')" />
    <div class="list-menu">
      <div class="menu menu--primary">
        <router-link :to="{ name: 'collectionMedia' }" v-text="t('catalog.ct.media', 2)" />
        <router-link :to="{ name: 'collectionPlaylists' }" v-text="t('catalog.ct.playlist', 2)" />
        <router-link :to="{ name: 'collectionArtists' }" v-text="t('catalog.ct.artist', 2)" />
      </div>
      <div class="menu menu--secondary">
        <router-view name="searchbar" />
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
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/title";
@use "@/style/elements/list-menu";

.collection {
  margin-bottom: 12rem;
}

.title {
  @include title.default;
}

.list-menu {
  @include container.default;
  @include list-menu.default;
}
</style>

<script type="ts">
import { defineComponent, onActivated, onUpdated, ref } from 'vue';
import { useI18n } from "vue-i18n";

import Searchbar from '@/components/filter/Searchbar.vue';

export default defineComponent({
  props: {
    filter: {
      type: Object,
      required: false,
    },
  },
  components: {
    Searchbar,
  },
  setup() {
    const { t } = useI18n();
    const menuRef = ref(null);
    const setMenuFocus = () => {
      const el = menuRef.value.querySelector('.router-link-exact-active');
      if (el) {
        el.scrollIntoView();
      }
    };
    onActivated(() => {
      setMenuFocus();
    });
    onUpdated(() => {
      setMenuFocus();
    });
    return {
      t,
      menuRef,
    };
  },
});
</script>

<template>
  <div>
    <div class="title">Discover</div>
    <div class="list-menu">
      <div ref="menuRef" class="menu menu--primary">
        <!--
        <router-link :to="{ name: 'discoverHome' }" v-text="t('menu.discover')" />
        -->
        <router-link :to="{ name: 'discoverMoods' }" v-text="t('catalog.ct.mood')" />
        <router-link :to="{ name: 'discoverMedia' }" v-text="t('catalog.ct.media', 2)" />
        <router-link :to="{ name: 'discoverPlaylists' }" v-text="t('catalog.ct.playlist', 2)" />
        <router-link :to="{ name: 'discoverArtists' }" v-text="t('catalog.ct.artist', 2)" />
        <router-link :to="{ name: 'discoverEditors' }" v-text="t('broadcast.ct.editor', 2)" />
      </div>
      <div class="menu menu--secondary">
        <Searchbar v-if="filter" :filter="filter" />
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/title";
@use "@/style/elements/list-menu";

.title {
  @include title.default;
}

.list-menu {
  @include container.default;
  @include list-menu.default;
}
</style>

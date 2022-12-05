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
  <div class="main-menu">
    <router-link to="/" v-text="t('menu.home')" />
    <router-link to="/discover/" v-text="t('menu.discover')" />
    <router-link to="/collection/" v-text="t('menu.collection')" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";

.main-menu {
  color: inherit;

  > a {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 150px;
    height: 100%;
    padding: 0 2rem;
    text-decoration: none;
    border-right: 1px solid transparent;
    border-left: 1px solid transparent;
    transition: color, background-color 10ms, border-color 100ms;
    @include live-color.fg;

    &:hover {
      background: rgb(var(--c-page-fg) 0.1);
      transition: color, background-color 200ms;
    }

    &.router-link-active {
      @include live-color.fg-inverse;
      @include live-color.bg-inverse;

      transition: color, background-color 200ms;
    }

    &:not(&.router-link-active) {
      border-left-color: rgb(var(--c-page-fg) 0.2);

      &:last-child {
        border-right-color: rgb(var(--c-page-fg) 0.2);
      }
    }
  }
}
</style>

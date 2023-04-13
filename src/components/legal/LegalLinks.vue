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
  <nav class="legal-links">
    <div class="link-group">
      <router-link to="/legal/dpp/" v-text="t('menu.dpp')" />
      <router-link to="/legal/terms/" v-text="t('menu.terms')" />
    </div>
  </nav>
</template>

<style lang="scss" scoped>
@use "@/style/base/live-color";

.legal-links {
  @include live-color.bg;

  position: fixed;
  z-index: 99;
  width: 100%;
  bottom: 0;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  font-size: var(--t-fs-small);
  font-weight: 300;
  border-top: 1px solid rgb(var(--c-page-fg) / 20%);

  > .link-group {
    display: flex;
    align-items: flex-end;
    padding: 0.25rem 0 0.5rem;
    justify-content: center;

    > a {
      @include live-color.fg;

      padding: 4px 8px;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>
<script setup lang="ts"></script>

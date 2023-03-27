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
  <div class="playlist-row-header">
    <div class="container">
      <div class="label" />
      <div class="label label--playlist" v-text="`${t('catalog.ct.playlist')}:`" />
      <div class="label" v-text="`${t('broadcast.ct.editor')}:`" />
      <div class="label" v-text="`${t('text.airtime')}/${t('text.duration')}:`" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";

.playlist-row-header {
  background: rgb(var(--c-light));
  height: 41px;
  align-items: center;
  display: flex;
  border-bottom: 1px solid rgb(var(--c-dark) / 20%);

  [data-theme="dark"] & {
    border-bottom: 1px solid rgb(var(--c-dark) / 10%);
  }
}

.container {
  @include container.default;

  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-columns: 96px 16fr 10fr 6fr 96px;

  .label {
    &::first-letter {
      text-transform: uppercase;
    }

    &--playlist {
      margin-left: -48px;
    }
  }
}
</style>

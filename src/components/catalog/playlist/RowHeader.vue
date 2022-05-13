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
  <div class="media-row-header">
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
.media-row-header {
  background: rgb(var(--c-white));
  padding: 0.5rem 0;
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-columns: 96px 8fr 6fr 2fr 96px;
  .label {
    &:first-letter {
      text-transform: uppercase;
    }
    &--playlist {
      margin-left: -48px;
    }
  }
}
</style>

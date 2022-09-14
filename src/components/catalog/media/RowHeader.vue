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
      <div class="label label--track">
        <span v-text="t('catalog.ct.media')" />
      </div>
      <div class="label">
        <span v-text="t('catalog.ct.artist')" />
        <span v-text="t('catalog.ct.release')" />
      </div>
      <div class="label label--airtime">
        <span v-text="t('text.duration')" />
        <span v-text="t('text.airtime')" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.media-row-header {
  background: rgb(var(--c-white));
  height: 41px;
  align-items: center;
  display: flex;
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-columns: 96px 16fr 10fr 6fr 96px;
  .label {
    white-space: nowrap;
    > span {
      display: inline-block;
      &:first-letter {
        text-transform: uppercase;
      }
      &:not(:last-child) {
        &:after {
          content: "/";
        }
      }
      &:last-child {
        &:after {
          content: ":";
        }
      }
    }
    &--track {
      margin-left: -48px;
    }
    &--airtime {
      grid-column: span 2;
    }
  }
}
</style>

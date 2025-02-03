<script lang="ts" setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";

import NewsSurvey from "@/components/survey/NewsSurvey.vue";
import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import { usePlayerState } from "@/composables/player";

const { t } = useI18n();

const { isNews } = usePlayerState();

const overlayVisible = ref(false);
</script>

<i18n lang="yaml">
de:
  title: "Umfrage"
en:
  title: "Survey"
</i18n>

<template>
  <div @click="overlayVisible = !overlayVisible" class="news" :class="{ 'is-news': isNews }">
    <span class="news__text">News</span>
    <Teleport to="body">
      <OverlayPanel
        :is-visible="overlayVisible"
        @close="overlayVisible = false"
        :title="t('title')"
      >
        <NewsSurvey @close="overlayVisible = false" />
      </OverlayPanel>
    </Teleport>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.news {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.5rem;
  border-radius: 0.75rem;
  padding: 0 0.75rem;
  border: 1px solid rgb(var(--c-fg) / 25%);
  transition: border 100ms, background 100ms;
  cursor: pointer;
  min-width: 48px;

  &__text {
    @include typo.small;

    color: rgb(var(--c-fg));
  }

  @include responsive.on-hover {
    background: rgb(var(--c-fg) / 12.5%);
    border-color: transparent;
  }

  &.is-news {
    background: rgb(var(--c-red));
  }
}
</style>

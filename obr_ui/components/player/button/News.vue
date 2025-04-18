<script lang="ts" setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import NewsSettings from "@/components/news/NewsSettings.vue";
import SlideUpPanel from "@/components/ui/panel/SlideUpPanel.vue";
import { useNews } from "@/composables/news";
import { usePlayerState } from "@/composables/player";

const { t } = useI18n();

const { isNews } = usePlayerState();

const { provider, endPlayNews } = useNews();

const overlayVisible = ref(false);

const skipVisible = computed(() => isNews && provider.value);
</script>

<i18n lang="yaml">
de:
  title: "Choose your News!"
en:
  title: "Choose your News!"
</i18n>

<template>
  <div @click="overlayVisible = !overlayVisible" class="news" :class="{ 'is-news': isNews }">
    <span class="news__text">News</span>
    <Teleport to="body">
      <SlideUpPanel
        :is-visible="overlayVisible"
        @close="overlayVisible = false"
        :title="t('title')"
      >
        <NewsSettings />
        <template #footer>
          <div
            class="controls"
            :style="{
              '--c-fg': 'var(--c-white)',
            }"
          >
            <div v-if="provider" class="selected-provider">
              Selected Service: <em>{{ provider }}</em>
            </div>
            <div v-else class="selected-provider">No Service Selected</div>
            <button
              v-if="skipVisible"
              class="button"
              :disabled="!isNews"
              @click.prevent="endPlayNews()"
            >
              Skip News
            </button>
          </div>
        </template>
      </SlideUpPanel>
    </Teleport>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";
@use "@/style/elements/button";

@keyframes pulse {
  0% {
    transform: scale(0.975);
  }

  30% {
    transform: scale(1.05);
  }

  100% {
    transform: scale(0.975);
  }
}

.news {
  position: relative;
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
    border-color: rgb(var(--c-red));
    transform: scale(1);
    animation: pulse 1s infinite;
  }
}

.controls {
  min-height: 4rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 2rem;

  .selected-provider {
    flex-grow: 1;

    > em {
      text-transform: uppercase;
      font-style: normal;
    }
  }

  .button {
    @include button.outlined(3rem);
  }
}
</style>

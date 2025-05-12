<script lang="ts" setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import NewsSettings from "@/components/news/NewsSettings.vue";
import SlideUpPanel from "@/components/ui/panel/SlideUpPanel.vue";
import { useNews } from "@/composables/news";
import { usePlayerControls, usePlayerState } from "@/composables/player";

const { t } = useI18n();

const { isNews } = usePlayerState();
const { endPlayNews } = usePlayerControls();

const { selectedProvider: provider } = useNews();

const overlayVisible = ref(false);

const skipVisible = computed(() => isNews && provider.value);
</script>

<i18n lang="yaml">
de:
  title: "News Einstellungen"
en:
  title: "News Settings"
</i18n>

<template>
  <div
    @click="overlayVisible = !overlayVisible"
    class="news"
    :class="{ 'is-news': isNews }"
    data-cta-target="news"
  >
    <span class="news__text">News</span>
    <Teleport to="body">
      <SlideUpPanel
        :is-visible="overlayVisible"
        @close="overlayVisible = false"
        :title="t('title')"
      >
        <div class="body">
          <div class="info">
            <p>
              We're seeking your input to enhance our radio programming. We're considering
              introducing a new feature – an option that allows you to access daily news updates.
            </p>
          </div>
          <NewsSettings />
        </div>
        <template #footer>
          <div
            class="controls"
            :style="{
              '--c-fg': 'var(--c-white)',
            }"
          >
            <div v-if="provider" class="selected-provider">
              Selected Service:
              <em>
                <span>{{ provider.title }}</span>
                <span v-if="provider.language"> ({{ provider.language }})</span>
              </em>
              <a class="link" :href="`https://${provider.url}`" target="_blank">
                <span>{{ provider.url }}</span>
              </a>
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

.body {
  > .info {
    > p {
      max-width: 760px;
    }
  }
}

.controls {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  border-top: 1px solid rgb(var(--c-fg));

  .selected-provider {
    flex-grow: 1;

    > em {
      font-style: normal;
    }

    > a {
      &::before {
        content: "●";
        padding-left: 0.5rem;
        padding-right: 0.5rem;
      }

      > span {
        text-decoration: underline;
      }
    }
  }

  .button {
    @include button.outlined(3rem);
  }
}
</style>

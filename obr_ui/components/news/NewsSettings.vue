<script lang="ts" setup>
import { computed, ref } from "vue";
import type { AxiosError } from "axios";

import Debug from "@/components/dev/Debug.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import { useAccount } from "@/composables/account";
import { useNews } from "@/composables/news";
import { usePlayerControls, usePlayerState } from "@/composables/player";

const { settings } = useAccount();

const { isNews } = usePlayerState();
const { playLive, playNews, endPlayNews } = usePlayerControls();

const NEWS_PROVIDERS = [
  {
    key: "srf",
    title: "SRF News",
    language: "DE",
    description:
      "Nachrichten aus den Bereichen US-Wahlen 2024, Ukraine, Klima, Schweiz, International, Wirtschaft, Gesellschaft und Ratgeber",
    url: "https://www.srf.ch/news",
  },
  {
    key: "bbc",
    title: "BBC",
    language: "EN",
    description: "BBC News",
    url: "https://www.bbc.co.uk/news",
  },
];

const providers = computed(() => {
  return NEWS_PROVIDERS;
});

const { provider: newsProvider } = useNews();

const errors = ref<Array<string | AxiosError>>([]);

const setProvider = async (providerKey: string) => {
  if (newsProvider.value === providerKey) {
    newsProvider.value = ""; // NOTE: this is ugly, it should rather be `null`
  } else {
    newsProvider.value = providerKey;
  }
};
</script>
<template>
  <div class="news-settings">
    <div class="input-container providers">
      <label v-for="provider in providers" :key="`${provider.key}-input`" class="provider">
        <input
          class="input"
          type="checkbox"
          name="providers"
          :checked="newsProvider === provider.key"
          @change="setProvider(provider.key)"
        />
        <span class="title" v-text="provider.title" />
        <span class="description" v-text="provider.description" />
        <a class="link" v-text="provider.url" :href="provider.url" target="_blank" />
      </label>
    </div>
    <div class="form-errors" v-if="errors.length">
      <ApiErrors :errors="errors" />
    </div>
    <Debug :value="{ settings, isNews }">
      <div class="actions">
        <button @click.prevent="playLive()">Trigger Live</button>
        <button @click.prevent="playNews('srf')">Trigger News</button>
        <button @click.prevent="endPlayNews()">End News</button>
      </div>
    </Debug>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";
@use "@/style/elements/form";

.providers {
  background: transparent;
}

.news-settings {
  @include form.default;

  .providers {
    display: flex;
    flex-direction: column;

    .provider {
      display: grid;
      grid-template-areas:
        "checkbox title"
        "checkbox description"
        "checkbox link";
      grid-template-columns: 36px 1fr;
      grid-column-gap: 1rem;
      margin-bottom: 1rem;

      > input {
        height: 36px;
        width: 36px;
        grid-area: checkbox;
        align-self: start;
        margin-top: 4px;
      }

      > .title {
        grid-area: title;

        @include typo.large;
      }

      > .description {
        grid-area: description;
        margin-top: 0.5rem;
      }

      > .link {
        grid-area: link;
        text-decoration: underline;
        margin-top: 0.5rem;
      }
    }
  }
}
</style>

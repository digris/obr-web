<script lang="ts" setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import type { AxiosError } from "axios";

import { updateSettings } from "@/api/account";
import Debug from "@/components/dev/Debug.vue";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import { useAccount } from "@/composables/account";
import { usePlayerControls, usePlayerState } from "@/composables/player";

const { settings } = useAccount();

const { isNews } = usePlayerState();
const { playLive, playNews, endPlayNews } = usePlayerControls();

const { t } = useI18n();

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

const setProvider = (providerKey: string) => {
  if (settings.value.newsProvider === providerKey) {
    settings.value.newsProvider = ""; // NOTE: this is ugly, it should rather be `null`
  } else {
    settings.value.newsProvider = providerKey;
  }
};

const errors = ref<Array<string | AxiosError>>([]);

const submitForm = async () => {
  errors.value = [];
  try {
    await updateSettings(settings.value);
  } catch (err: unknown) {
    console.error(err);
    const error = err as AxiosError;
    errors.value = [error];
  }
};
</script>
<template>
  <div>
    <form class="form" @submit.prevent="submitForm">
      <div class="input-container providers">
        <label v-for="provider in providers" :key="`${provider.key}-input`" class="provider">
          <input
            class="input"
            type="checkbox"
            name="providers"
            :checked="settings.newsProvider === provider.key"
            @change="setProvider(provider.key)"
          />
          <span class="title" v-text="provider.title" />
          <span class="description" v-text="provider.description" />
        </label>
      </div>
      <div class="form-errors" v-if="errors.length">
        <ApiErrors :errors="errors" />
      </div>
      <div class="input-container submit">
        <AsyncButton class="button" @click.prevent="submitForm">
          {{ t("formActions.save") }}
        </AsyncButton>
      </div>
    </form>
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

.form {
  @include form.default;

  .providers {
    display: flex;
    flex-direction: column;

    .provider {
      display: grid;
      grid-template-areas:
        "checkbox title"
        "checkbox description";
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

        @include typo.dim;
      }
    }
  }
}
</style>

<script lang="ts" setup>
import { ref } from "vue";
import type { AxiosError } from "axios";

import Debug from "@/components/dev/Debug.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import { useAccount } from "@/composables/account";
import { useAnalytics } from "@/composables/analytics";
import { useNews } from "@/composables/news";
import { usePlayerControls, usePlayerState } from "@/composables/player";

const { settings } = useAccount();

const { isNews } = usePlayerState();
const { playNews, endPlayNews } = usePlayerControls();
const { logUIEvent } = useAnalytics();

const { providers, selectedProvider, setProvider } = useNews();

const errors = ref<Array<string | AxiosError>>([]);

const toggleProvider = async (key: string) => {
  if (providers.value.find((provider) => provider.key === key)?.enabled === false) {
    return;
  }

  if (selectedProvider.value?.key === key) {
    setProvider(null);
    logUIEvent("news:disable");
  } else {
    setProvider(key);
    logUIEvent("news:enable", key);
  }
};
</script>
<template>
  <div class="news-settings">
    <div class="info">
      <p>Wähle deinen News-Service:</p>
    </div>
    <div class="providers">
      <div
        v-for="provider in providers"
        :key="`${provider.key}-input`"
        class="provider"
        :class="{
          'is-enabled': provider.enabled,
          'is-selected': provider.selected,
        }"
        @click="toggleProvider(provider.key)"
      >
        <div class="title">
          <span class="title__name" v-text="provider.title" />
          <span v-if="provider.language" class="title__language" v-text="provider.language" />
          <span v-if="!provider.enabled" class="title__disabled" v-text="`coming soon`" />
        </div>
        <div class="description">
          <p v-text="provider.description" />
        </div>
        <a class="link" v-text="provider.url" :href="`https://${provider.url}`" target="_blank" />
      </div>
    </div>
    <div class="actions">
      <div>
        <div
          class="unset-provider"
          :class="{
            'is-selected': !selectedProvider,
          }"
          @click="setProvider(null)"
        >
          <div class="checkbox" type="checkbox" />
          <span class="label">Keine News einblenden</span>
        </div>
      </div>
    </div>
    <div class="form-errors" v-if="errors.length">
      <ApiErrors :errors="errors" />
    </div>
    <Debug :value="{ settings, isNews }">
      <div class="actions">
        <button @click.prevent="playNews('rfi')">Trigger News</button>
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
  .info {
    padding: 2rem 0 1rem;
  }

  .providers {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-gap: 1rem;

    .provider {
      cursor: pointer;
      background: rgb(var(--c-fg) / 20%);
      padding: 0.5rem;
      border: 1px solid rgb(var(--c-fg) / 5%);
      border-radius: 0.25rem;
      transition: 60ms background ease-in-out;

      .title {
        display: flex;

        &__language {
          margin-left: 0.25rem;

          &::before {
            content: "(";
          }

          &::after {
            content: ")";
          }
        }

        &__disabled {
          flex-grow: 1;
          text-align: end;
        }
      }

      .description {
        @include typo.dim;

        white-space: pre-line;
      }

      .link {
        display: none;
      }

      &:not(.is-enabled) {
        cursor: not-allowed;

        .title {
          &__name,
          &__language {
            @include typo.dim;
          }

          &__disabled {
            color: rgb(var(--c-green) / 100%);
            opacity: 1;
          }
        }
      }

      &.is-selected {
        background: rgb(var(--c-green) / 100%);
      }
    }
  }

  .actions {
    padding: 1.25rem 0 4rem;

    .unset-provider {
      display: flex;
      align-items: center;
      gap: 1rem;
      cursor: pointer;

      > .checkbox {
        position: relative;
        height: 36px;
        width: 36px;
        grid-area: checkbox;
        align-self: start;
        border: 2px solid rgb(var(--c-fg) / 100%);
        border-radius: 0.25rem;
        display: flex;
        align-items: center;
        justify-content: center;

        &::before {
          content: "";
          display: flex;
          height: 1rem;
          width: 1rem;
          transform: scale(0);
          transition: 60ms transform ease-in-out, 60ms background ease-in-out;
          background: rgb(var(--c-fg) / 100%);
          border-radius: 1px;
        }
      }

      .label {
        @include typo.default;
      }

      &.is-selected {
        > .checkbox {
          background: rgb(var(--c-green));

          &::before {
            transform: scale(1);
          }
        }
      }
    }
  }
}
</style>

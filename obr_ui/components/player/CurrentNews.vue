<script lang="ts" setup>
import { computed } from "vue";

import iconRFI from "@/assets/news/icon-rfi.png";
import { useNews } from "@/composables/news";

const { selectedProvider: provider } = useNews();

const iconSrc = computed(() => {
  if (!provider.value) {
    return "";
  }
  if (provider.value.key === "rfi") {
    return iconRFI;
  }
  return "";
});
</script>

<template>
  <div v-if="provider" class="current-news">
    <div class="visual">
      <img v-if="iconSrc" :src="iconSrc" />
    </div>
    <div class="metadata">
      <div class="metadata--primary">
        {{ provider.key }}
      </div>
      <div class="metadata--secondary">
        <a
          :href="`https://${provider.url}`"
          v-text="provider.url"
          target="_blank"
          rel="noopener noreferrer"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.current-news {
  display: grid;
  grid-template-columns: 64px 1fr;

  .visual {
    height: 3rem;
    width: 3rem;

    > img {
      height: 100%;
      width: 100%;
    }
  }

  .metadata {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    &--primary {
      text-transform: uppercase;
    }

    &--primary,
    &--secondary {
      max-width: 100%;
      overflow: inherit;
      white-space: inherit;
      text-overflow: inherit;

      > a {
        text-decoration: underline;
      }
    }
  }
}
</style>

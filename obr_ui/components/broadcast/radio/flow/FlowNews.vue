<script lang="ts" setup>
import { useNews } from "@/composables/news";

defineProps({
  itemSize: {
    type: Number,
    default: 0,
  },
});

const { selectedProvider: provider } = useNews();
</script>

<template>
  <div
    class="flow-news"
    :style="{
      '--item-size': `${itemSize}px`,
    }"
  >
    <div class="panel">
      <div v-if="provider" class="item">
        <div class="label">News</div>
        <div class="provider">
          <div class="provider__key" v-text="provider.key" />
          <div class="provider__title" v-text="provider.title" />
          <div class="provider__link">
            <a
              :href="`https://${provider.url}`"
              v-text="provider.url"
              target="_blank"
              rel="noopener noreferrer"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/mixins";
@use "@/style/base/typo";

.flow-news {
  top: 0;
  position: absolute;
  height: var(--item-size);
  width: 100%;
  z-index: 15;

  > .panel {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    > .item {
      flex: 0 0 var(--item-size);
      flex-direction: column;
      height: var(--item-size);
      width: var(--item-size);
      margin: 60px 0;
      display: flex;
      background: rgb(70 70 70 / 100%);
      box-shadow: 0 0 20px rgb(0 0 0 / 50%);
      padding: 1rem 1rem 1rem 2rem;
      color: rgb(var(--c-white));

      > .label {
        &::after {
          content: ":";
        }
      }

      .provider {
        padding-top: 2rem;

        &__key {
          @include typo.x-large;
          @include typo.bold;

          text-transform: uppercase;
        }

        &__link {
          > a {
            text-decoration: underline;
          }
        }
      }
    }
  }
}
</style>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useSettingsStore } from "@/stores/settings";
import { useDevice } from "@/composables/device";

import Section from "./Section.vue";

const BANDWITH_CHOICES = [
  {
    value: 720000,
    title: "512 Kb/s",
    description: "HiFi · 200 Mb/h",
  },
  {
    value: 200000,
    title: "128 Kb/s",
    description: "Eco · 50 Mb/h",
  },
  // {
  //   value: 56000,
  //   title: "36 Kb/s",
  //   description: "Super-Eco: 15 Mb/h",
  // },
];

export default defineComponent({
  components: {
    Section,
  },
  setup() {
    const { t } = useI18n();
    const { isDesktop } = useDevice();
    const maxBandwidthChoices = BANDWITH_CHOICES;
    const settingsStore = useSettingsStore();
    const maxBandwidth = computed(() => settingsStore.maxBandwidth);
    const setMaxBandwidth = (value: number) => {
      settingsStore.setMaxBandwidth(value);
    };
    return {
      t,
      isDesktop,
      maxBandwidth,
      maxBandwidthChoices,
      setMaxBandwidth,
    };
  },
});
</script>

<template>
  <Section :title="t('account.settings.stream.title')" :outlined="false">
    <div class="info">
      <i18n-t v-if="isDesktop" keypath="account.settings.stream.infoLong" tag="p" />
      <i18n-t keypath="account.settings.stream.infoShort" tag="p" />
    </div>
    <div class="options options--bw">
      <div
        v-for="choice in maxBandwidthChoices"
        :key="choice.value"
        @click.prevent="setMaxBandwidth(choice.value)"
        class="option"
        :class="{ 'is-current': choice.value === maxBandwidth }"
      >
        <p class="title" v-text="choice.title" />
        <p class="description" v-text="choice.description" />
      </div>
    </div>
  </Section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
.info {
  padding: 0 2rem 1rem 0;
  opacity: 0.5;
  white-space: pre-line;
  @include responsive.bp-medium {
    @include typo.small;
  }
}
.options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 1rem;
  .option {
    cursor: pointer;
    padding: 0.5rem;
    background: rgb(var(--c-white));
    border: 1px solid rgb(var(--c-gray-200));
    border-radius: 3px;
    transition: background 200ms;
    &:hover {
      background: rgba(var(--c-black), 0.1);
    }
    &.is-current {
      color: rgb(var(--c-white));
      background: rgb(var(--c-green));
      border-color: rgb(var(--c-green));
    }
  }
  @include responsive.bp-medium {
    grid-template-columns: unset;
    grid-gap: 0.5rem;
    .option {
      display: flex;
      .title {
        flex-grow: 1;
      }
    }
  }
}
</style>

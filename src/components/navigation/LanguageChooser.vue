<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useSettingsStore } from "@/stores/settings";

export default defineComponent({
  setup() {
    const settingsStore = useSettingsStore();
    const { locale, availableLocales } = useI18n({ useScope: "global" });
    const setLocale = (value: string) => {
      locale.value = value;
      settingsStore.setLocale(value);
      // NOTE: refresh is only needed to also update resources loaded via API
      document.location.reload();
    };
    return {
      currentLocale: locale,
      availableLocales,
      setLocale,
    };
  },
});
</script>

<template>
  <div class="language-chooser">
    <a
      v-for="(locale, index) in availableLocales"
      :key="`locale-${index}-${locale}`"
      @click.prevent="setLocale(locale)"
      href="#"
      class="language"
      :class="{ 'is-current': locale === currentLocale }"
    >
      <span v-text="locale" />
    </a>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.language-chooser {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  .language {
    @include typo.tiny;
    @include typo.uppercase;
    height: 24px;
    width: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    span {
      border-bottom: 2px solid transparent;
    }
    &:hover,
    &.is-current {
      span {
        border-bottom-color: currentColor;
      }
    }
  }
}
</style>

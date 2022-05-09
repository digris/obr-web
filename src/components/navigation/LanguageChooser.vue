<script lang="ts">
import { defineComponent } from "vue";
import { useLanguage } from "@/composables/language";

export default defineComponent({
  setup() {
    const languages = ["de", "en", "fr"];
    const { currentLanguage, setLanguage } = useLanguage();
    return {
      currentLanguage,
      languages,
      setLanguage,
    };
  },
});
</script>
<template>
  <div class="language-chooser">
    <a
      v-for="(language, index) in languages"
      :key="`language-${index}-${language}`"
      @click.prevent="setLanguage(language)"
      href="#"
      class="language"
      :class="{ 'is-current': language === currentLanguage }"
    >
      <span v-text="language" />
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

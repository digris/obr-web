<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { useDevice } from "@/composables/device";

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      default: "",
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { isMobile } = useDevice();
    const q = computed({
      get: () => props.modelValue,
      set: (value: string) => emit("update:modelValue", value),
    });
    const searchInput = ref<HTMLInputElement | null>(null);
    onMounted(() => {
      searchInput.value?.focus();
      if (isMobile) {
        // scroll to top after displaying on-screen keyboard
        setTimeout(() => {
          window.scrollTo(0, 0);
        }, 100);
      }
    });
    return {
      t,
      q,
      searchInput,
      close,
    };
  },
});
</script>
<template>
  <div class="search-input">
    <input ref="searchInput" v-model="q" type="text" :placeholder="t('search.search')" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.search-input {
  > input {
    @include typo.large;
    @include typo.bold;

    color: rgba(var(--c-dark) / 100%);
    background: rgba(var(--c-light) / 100%);
    border: none;
    width: 100%;

    &:focus {
      outline: none;
    }

    &::placeholder {
      color: rgb(var(--c-dark) / 20%);
    }
  }
}
</style>

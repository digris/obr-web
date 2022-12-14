<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

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
    const q = computed({
      get: () => props.modelValue,
      set: (value: string) => emit("update:modelValue", value),
    });
    const searchInput = ref<HTMLInputElement | null>(null);
    onMounted(() => searchInput.value?.focus());
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

    border: none;
    width: 100%;

    &:focus {
      outline: none;
    }

    &::placeholder {
      color: rgb(var(--c-black) / 20%);
    }
  }
}
</style>

<script type="ts">
import { computed, defineComponent, watch } from 'vue';
import { storeToRefs } from "pinia";

import { useSettingsStore } from "@/stores/settings";

const DARK_VALUE = "dark"
const DATA_ATTRIBUTE = "data-theme"

export default defineComponent({
  components: {},
  setup() {
    const { theme } = storeToRefs(useSettingsStore());
    const isDark = computed(() => theme.value === DARK_VALUE);
    const toggleMode = () => (isDark.value) ? theme.value = null : theme.value = DARK_VALUE;
    watch(
      () => theme.value,
      (value) => {
        if (value) {
          document.body.setAttribute(DATA_ATTRIBUTE, value);
        } else {
          document.body.removeAttribute(DATA_ATTRIBUTE);
        }
      }
    );
    return {
      theme,
      isDark,
      toggleMode,
    };
  },
});
</script>

<template>
  <label class="toggle-mode" :class="{ 'is-dark': isDark }">
    <span class="outline"></span>
    <span class="label">Darkmode</span>
    <input class="toggle" type="checkbox" @change="toggleMode" />
  </label>
</template>

<style lang="scss" scoped>
.toggle-mode {
  cursor: pointer;
  height: 30px;
  display: grid;
  grid-template-columns: 54px auto auto;
  grid-column-gap: 0.5rem;

  > input {
    opacity: 0;
    width: 0;
  }

  .outline {
    position: relative;
    cursor: pointer;
    background-color: rgb(var(--c-fg));
    transition: 200ms;
    border-radius: 30px;

    &::before {
      position: absolute;
      content: "";
      height: 24px;
      width: 24px;
      left: 3px;
      bottom: 3px;
      background-color: rgb(var(--c-bg));
      transition: 200ms;
      border-radius: 50%;
    }
  }

  &.is-dark {
    .outline {
      &::before {
        left: 27px;
      }
    }
  }

  .label {
    line-height: 30px;
  }
}
</style>

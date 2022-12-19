<script type="ts">
import { defineComponent, watch } from 'vue';
import { storeToRefs } from "pinia";

import { useSettings } from "@/composables/settings";
import { useSettingsStore } from "@/stores/settings";

const DATA_ATTRIBUTE = "data-th" +
  "eme"

export default defineComponent({
  components: {},
  setup() {
    const { darkMode, setDarkMode } = useSettings();
    const { theme } = storeToRefs(useSettingsStore());
    const toggleMode = () => (darkMode.value) ? setDarkMode(false) : setDarkMode(true);
    watch(
      () => darkMode.value,
      (value) => {
        console.debug("DM", value);
        if (value) {
          document.body.setAttribute(DATA_ATTRIBUTE, "dark");
        } else {
          document.body.removeAttribute(DATA_ATTRIBUTE);
        }
      }
    );
    return {
      theme,
      darkMode,
      toggleMode,
    };
  },
});
</script>

<template>
  <label class="toggle-mode" :class="{ 'is-dark': darkMode }">
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

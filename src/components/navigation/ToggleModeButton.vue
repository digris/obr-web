<script type="ts">
import { defineComponent } from 'vue';
import { useDark } from '@vueuse/core'

export default defineComponent({
  components: {},
  setup() {
    const isDark = useDark()
    const toggleMode = (e) => {
      console.debug('toggleMode', e);
    }
    return {
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
    <input class="toggle" type="checkbox" v-model="isDark" />
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
    &:before {
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
      &:before {
        left: 27px;
      }
    }
  }
  .label {
    line-height: 30px;
  }
}
</style>

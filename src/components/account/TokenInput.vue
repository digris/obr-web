<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";

export default defineComponent({
  props: {
    valid: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["input"],
  setup(props, { emit }) {
    const inputEl = ref(null);
    const inputValue = ref("");
    const parseInput = (value: string) => {
      if (value.length >= 4 && value[3] !== "-") {
        value = [value.slice(0, 3), "-", value.slice(3)].join("");
      }
      return value.toUpperCase();
    };
    const handleInput = (e: any) => {
      const value = parseInput(e.target.value);
      inputValue.value = value;
      emit("input", value);
    };
    onMounted(() => {
      // @ts-ignore
      inputEl.value.focus();
    });
    return {
      inputEl,
      inputValue,
      handleInput,
    };
  },
});
</script>

<template>
  <div class="token-input" :class="{ 'is-valid': valid }">
    <div class="input-container token-input">
      <i18n-t keypath="account.auth.loginToken" tag="label" for="ti-1298" />
      <input
        ref="inputEl"
        id="ti-1298"
        class="input"
        @keyup="handleInput"
        :value="inputValue"
        maxlength="7"
        placeholder="Login-Code"
        autocomplete="one-time-code"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";

.token-input {
  @include form.default;

  .input-container {
    @include form.top-label;

    > label {
      white-space: nowrap;

      &::after {
        content: ":";
      }
    }
  }

  .input {
    @include form.input;

    font-size: 200%;
    transition: background 200ms;
  }

  &.is-valid {
    .input {
      background: rgb(var(--c-success) / 10%);
      border-color: rgb(var(--c-success) / 100%);
    }
  }
}
</style>

<script lang="ts">
import { defineComponent, ref } from 'vue';

const tokenRegex = new RegExp('^([A-Za-z0-9]{3})-([A-Za-z0-9]{3})$');

export default defineComponent({
  props: {
    token: {
      type: String,
      required: true,
    },
  },
  emits: [
    'input',
  ],
  setup(props, { emit }) {
    const inputValue = ref('');
    const inputValid = ref(false);
    const parseInput = (value: string) => {
      return value.toUpperCase();
    };
    const validateInput = (value: string) => {
      inputValid.value = tokenRegex.test(value);
    };
    const handleInput = (e: any) => {
      const value = parseInput(e.target.value);
      validateInput(value);
      inputValue.value = value;
      emit('input', value);
    };
    return {
      inputValue,
      inputValid,
      handleInput,
    };
  },
});
</script>

<template>
  <div
    class="token-input"
    :class="{'is-valid': inputValid}"
  >
    <input
      class="input"
      @keyup="handleInput"
      :value="inputValue"
      maxlength="7"
      placeholder="___-___"
      autocomplete="one-time-code"
    >
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";
.token-input {
  @include form.default;
  //width: 100%;
  .input {
    @include form.input;
    font-size: 200%;
    text-align: center;
    transition: background 200ms;
  }
  &.is-valid {
    .input {
      color: rgb(var(--c-black));
      //border-color: rgb(var(--c-success));
      background: rgba(var(--c-success), 0.1);
    }
  }
}
</style>

<script lang="ts">
import {
  defineComponent,
  onMounted,
  ref,
} from 'vue';

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
    const inputEl = ref(null);
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
    onMounted(() => {
      // @ts-ignore
      inputEl.value.focus();
    });
    return {
      inputEl,
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
    <div
      class="input-container token-input"
    >
      <input
        ref="inputEl"
        id="ti-1298"
        class="input"
        @keyup="handleInput"
        :value="inputValue"
        maxlength="7"
        placeholder="Login-Code"
        autocomplete="one-time-code"
      >
      <label
        for="ti-1298"
      >
        Login-Code
      </label>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";
.token-input {
  @include form.default;
  .input-container {
    @include form.float-label;
  }
  //width: 100%;
  .input {
    @include form.input;
    font-size: 200%;
    //text-align: center;
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

<script lang="ts">
import {
  defineComponent,
  onMounted,
  ref,
} from 'vue';

export default defineComponent({
  props: {
    code: {
      type: String,
      required: false,
      default: '',
    },
    valid: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: [
    'input',
  ],
  setup(props, { emit }) {
    const inputEl = ref(null);
    const inputValue = ref(props.code);
    const parseInput = (value: string) => {
      return value.toUpperCase();
    };
    const handleInput = async (e: any) => {
      const value = parseInput(e.target.value);
      inputValue.value = value;
      emit('input', value);
    };
    onMounted(() => {
      handleInput({
        target: {
          value: inputValue.value,
        },
      });
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
  <div
    class="code-input"
    :class="{'is-valid': valid}"
  >
    <input
      ref="inputEl"
        id="ti-1299"
      class="input"
      @keyup="handleInput"
      :value="inputValue"
      maxlength="8"
      placeholder="Code"
    >
      <label
        for="ti-1299"
      >
        Code
      </label>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";
.code-input {
  @include form.default;
  .input {
    @include form.input;
    font-size: 200%;
    transition: background 200ms;
  }
  &.is-valid {
    .input {
      background: rgba(var(--c-success), 0.1);
      border-color: rgb(var(--c-success));
    }
  }
}
</style>

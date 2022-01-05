<script lang="ts">
import {
  defineComponent,
  ref,
} from 'vue';

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      default: '',
      required: true,
    },
    type: {
      type: String,
      default: 'text',
    },
    label: {
      type: String,
      default: '',
    },
    autocomplete: {
      type: String,
      default: 'none',
    },
    placeholder: {
      type: String,
      default: '',
    },
    minlength: {
      type: Number,
      default: 0,
    },
    maxlength: {
      type: Number,
      default: 128,
    },
  },
  emits: [
    'keyup',
    'change',
    'update:modelValue',
  ],
  setup(props, { emit }) {
    const id = ref(`form-text-input-${Math.random().toString(36).slice(2)}`);
    const update = (value: string) => {
      emit('update:modelValue', value);
    };
    return {
      id,
      update,
    };
  },
});
</script>

<template>
  <div
    class="text-input"
  >
    <label
      v-if="label"
      :for="id"
      v-text="label"
    />
    <input
      :id="id"
      :value="modelValue"
      :type="type"
      :autocomplete="autocomplete"
      :minlength="`${minlength}`"
      :maxlength="`${maxlength}`"
      :placeholder="placeholder"
      @keyup="$emit('keyup')"
      @change="$emit('change')"
      @input="update($event.target.value)"
    >
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/form";
.text-input {
  display: grid;
  grid-template-rows: 1rem auto;
  gap: 1rem;
  color: rgb(var(--c-black));
  label {
    cursor: unset;
  }
  input {
    @include typo.large;
    @include typo.bold;
    display: grid;
    width: 100%;
    padding: 0.25em 0.5em;
    color: currentColor;
    border: 3px solid currentColor;
    border-radius: 3px;
    transition: 100ms background ease-in-out, 100ms border-color ease-in-out;
    &:focus {
      background: rgba(var(--c-black), 0.1);
      border-color: transparent;
      outline: none;
    }
    &:not(:valid) {
      background: rgba(var(--c-warning), 0.1);
    }
  }
}
</style>

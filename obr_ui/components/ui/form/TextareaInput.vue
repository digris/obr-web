<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      default: "",
      required: true,
    },
    label: {
      type: String,
      default: "",
      required: false,
    },
    maxlength: {
      type: Number,
      default: 128,
    },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const id = ref(`form-textarea-input-${Math.random().toString(36).slice(2)}`);
    const update = (value: string) => {
      emit("update:modelValue", value);
    };
    return {
      id,
      update,
    };
  },
});
</script>

<template>
  <div class="textarea-input">
    <label v-if="label" :for="id" v-text="label" />
    <textarea
      :id="id"
      :value="modelValue"
      :maxlength="maxlength"
      @input="update(($event.target as HTMLInputElement).value)"
    />
  </div>
</template>

<style lang="scss" scoped>
.textarea-input {
  display: grid;
  grid-template-rows: 1rem auto;
  gap: 1rem;
  color: rgb(var(--c-dark) / 100%);

  label {
    cursor: unset;
  }

  textarea {
    display: grid;
    width: 100%;
    min-height: 6rem;
    padding: 0.25em 0.5em;
    color: currentcolor;
    font-size: 2em;
    font-family: var(--font-family);
    border: 3px solid currentcolor;
    border-radius: 3px;
    transition: 100ms background ease-in-out, 100ms border-color ease-in-out;

    &:focus {
      background: rgb(var(--c-dark) / 10%);
      border-color: transparent;
      outline: none;
    }
  }
}
</style>

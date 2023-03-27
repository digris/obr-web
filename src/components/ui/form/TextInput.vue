<script lang="ts">
import { computed, defineComponent, ref } from "vue";

export default defineComponent({
  props: {
    modelValue: {
      type: [String, Number],
      default: "",
      required: true,
    },
    type: {
      type: String,
      default: "text",
    },
    label: {
      type: String,
      default: "",
    },
    errors: {
      type: Array,
      default: () => [],
    },
    autocomplete: {
      type: String,
      default: "none",
    },
    placeholder: {
      type: String,
      default: "",
    },
    minlength: {
      type: Number,
      default: 0,
    },
    maxlength: {
      type: Number,
      default: 128,
    },
    minValue: {
      type: Number,
      default: null,
    },
    maxValue: {
      type: Number,
      default: null,
    },
  },
  emits: ["keyup", "change", "update:modelValue"],
  setup(props, { emit }) {
    const id = ref(`form-text-input-${Math.random().toString(36).slice(2)}`);
    const update = (value: string) => emit("update:modelValue", value);
    const hasError = computed(() => props.errors.length > 0);
    return {
      id,
      update,
      hasError,
    };
  },
});
</script>

<template>
  <div class="text-input" :class="{ 'has-error': hasError }">
    <div class="top">
      <label v-if="label" :for="id" v-text="label" />
      <div v-if="errors.length" class="errors">
        <span v-for="(error, index) in errors" :key="`input-error-${id}-${index}`" v-text="error" />
      </div>
    </div>
    <input
      :id="id"
      :value="modelValue"
      :type="type"
      :autocomplete="autocomplete"
      :minlength="minlength"
      :maxlength="maxlength"
      :placeholder="placeholder"
      :min="minValue"
      :max="maxValue"
      @keyup="$emit('keyup')"
      @change="$emit('change')"
      @input="update($event.target.value)"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/form";

.text-input {
  display: grid;
  grid-template-rows: 1rem auto;
  column-gap: 1rem;
  row-gap: 1rem;
  color: rgb(var(--c-dark) / 100%);

  .top {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-gap: 1rem;
    align-items: center;

    label {
      cursor: unset;
    }

    .errors {
      @include typo.light;
      @include typo.small;

      color: rgb(var(--c-red) / 100%);
      text-align: right;

      @include responsive.bp-medium {
        display: none;
      }
    }
  }

  input {
    @include typo.large;
    @include typo.bold;

    display: grid;
    width: 100%;
    padding: 0.125em 0.5em;
    color: currentcolor;
    background: transparent;
    border: 1px solid rgb(var(--c-dark) / 20%);
    border-radius: 3px;
    transition: 100ms background ease-in-out, 100ms border-color ease-in-out;

    &:focus {
      background: rgb(var(--c-dark) / 10%);
      border-color: transparent;
      outline: none;
    }

    &:not(:valid) {
      background: rgb(var(--c-warning) / 10%);
    }
  }

  &.has-error {
    input {
      border-color: rgb(var(--c-red) / 100%);
    }
  }
}
</style>

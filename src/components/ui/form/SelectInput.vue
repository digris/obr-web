<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import type { PropType } from "vue";
// import { types } from 'sass';
// import Number = types.Number;

type Option = {
  value?: string;
  name?: string;
  selected?: boolean;
};

export default defineComponent({
  props: {
    modelValue: {
      type: [String, Number],
      default: null,
      required: true,
    },
    options: {
      type: Array as PropType<Array<Option>>,
      default: () => [],
    },
    label: {
      type: String,
      default: "",
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
  },
  emits: ["keyup", "change", "update:modelValue"],
  setup(props, { emit }) {
    const id = ref(`form-text-input-${Math.random().toString(36).slice(2)}`);
    const update = (value: string) => {
      emit("update:modelValue", value);
    };
    const annotatedOptions = computed(() => {
      return props.options.map((t: Option) => {
        return {
          ...t,
          selected: t.value === props.modelValue,
        };
      });
    });
    return {
      id,
      annotatedOptions,
      update,
    };
  },
});
</script>

<template>
  <div class="select-input">
    <label v-if="label" :for="id" v-text="label" />
    <select :id="id" :value="modelValue" @input="update($event.target.value)">
      <option
        v-for="option in annotatedOptions"
        :key="`${id}-${option.value}`"
        :value="option.value"
        :selected="modelValue === option.value"
        v-text="option.name"
      />
    </select>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/form";

.select-input {
  display: grid;
  grid-template-rows: 1rem auto;
  gap: 1rem;
  color: rgb(var(--c-black));

  label {
    cursor: unset;
  }

  select {
    @include typo.large;
    @include typo.bold;

    display: grid;
    width: 100%;
    padding: 0.25em 0.5em;
    color: currentcolor;
    background: transparent;
    border: 3px solid currentcolor;
    border-radius: 3px;
    transition: 100ms background ease-in-out, 100ms border-color ease-in-out;

    &:focus {
      background: rgb(var(--c-black) 0.1);
      border-color: transparent;
      outline: none;
    }
  }
}
</style>

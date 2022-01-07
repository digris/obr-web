<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
} from 'vue';

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      default: '',
      required: true,
    },
    name: {
      type: String,
      default: '',
      required: true,
    },
    value: {
      type: String,
      default: '',
      required: true,
    },
    label: {
      type: String,
      default: '',
      required: true,
    },
    size: {
      type: Number,
      default: 24,
    },
  },
  emits: [
    'update:modelValue',
  ],
  setup(props, { emit }) {
    const id = ref(`form-radio-input-${Math.random().toString(36).slice(2)}`);
    const isSelected = computed(() => {
      return props.value === props.modelValue;
    });
    const update = (value: string) => {
      emit('update:modelValue', value);
    };
    return {
      id,
      isSelected,
      update,
    };
  },
});
</script>

<template>
  <div
    class="radio-input"
    :style="{
      '--size': `${size}px`,
    }"
  >
    <input
      type="radio"
      :id="id"
      :name="name"
      :value="value"
      :checked="isSelected"
      @input="update($event.target.value)"
    />
    <label
      :for="id"
      v-text="label"
    />
    <!--
    <pre
      v-text="{
        modelValue,
        value,
        label,
        isSelected,
        id,
      }"
    />
    -->
  </div>
</template>

<style lang="scss" scoped>
.radio-input {
  display: grid;
  grid-template-columns: 1rem auto;
  gap: 1rem;
  line-height: 1.1;
  + .radio-input {
    margin-top: 0.5rem;
  }
  input[type=radio] {
    display: grid;
    width: var(--size);
    height: var(--size);
    margin: 0;
    color: currentColor;
    font: inherit;
    /* For iOS < 15 to remove gradient background */
    background-color: #fff;
    border: 3px solid currentColor;
    border-radius: 50%;
    cursor: pointer;
    appearance: none;
    place-content: center;
    &:before {
      width: var(--size);
      height: var(--size);
      border-radius: 50%;
      box-shadow: inset var(--size) var(--size) currentColor;
      transform: scale(0);
      transition: 50ms transform ease-in-out;
      content: "";
    }
    &:focus {
      outline: none;
    }
    &:checked::before {
      transform: scale(1);
    }
  }
  label {
    padding-top: 4px;
    cursor: pointer;
  }
}
</style>

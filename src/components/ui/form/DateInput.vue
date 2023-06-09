<script lang="ts">
import { defineComponent, ref } from "vue";

import IconProgram from "@/components/ui/icon/IconProgram.vue";

export default defineComponent({
  components: {
    IconProgram,
  },
  props: {
    modelValue: {
      type: String,
      default: "",
      required: true,
    },
    label: {
      type: String,
      default: "",
    },
    min: {
      type: String,
      default: "",
    },
    max: {
      type: String,
      default: "",
    },
  },
  emits: ["keyup", "change", "update:modelValue"],
  setup(props, { emit }) {
    const id = ref(`form-date-input-${Math.random().toString(36).slice(2)}`);
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
  <div class="date-input">
    <label v-if="label" :for="id" v-text="label" />
    <input
      :id="id"
      :value="modelValue"
      :min="min"
      :max="max"
      type="date"
      required
      @keyup="$emit('keyup')"
      @change="$emit('change')"
      @input="update(($event.target as HTMLInputElement).value)"
    />
    <div class="icon">
      <IconProgram :scale="0.825" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/form";

.date-input {
  position: relative;

  input {
    display: grid;
    height: 100%;
    grid-template-columns: 1fr 32px;
    width: 100%;
    padding: 0.25em 0.5em;
    color: currentcolor;
    border: 3px solid currentcolor;
    border-radius: 3px;
    transition: 100ms background ease-in-out, 100ms border-color ease-in-out;
    background: rgb(var(--c-light));

    &:focus {
      background: rgb(var(--c-dark) / 10%);
      border-color: transparent;
      outline: none;
    }

    &:hover {
      background: rgb(var(--c-dark) / 10%);
      outline: none;
      cursor: pointer;
    }

    &:not(:valid) {
      background: rgb(var(--c-warning) / 10%);
    }

    &::-webkit-calendar-picker-indicator {
      height: 100%;
      width: 30px;
      opacity: 0;
      z-index: 1;
      cursor: pointer;
    }
  }

  .icon {
    top: 0;
    position: absolute;
    height: 100%;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
  }
}
</style>

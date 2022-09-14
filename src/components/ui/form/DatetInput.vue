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
      @input="update($event.target.value)"
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
  //display: grid;
  position: relative;
  input {
    //@include typo.large;
    //@include typo.bold;
    display: grid;
    height: 100%;
    grid-template-columns: 1fr 32px;
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
    &:hover {
      background: rgba(var(--c-black), 0.1);
      //border-color: transparent;
      outline: none;
      cursor: pointer;
    }
    &:not(:valid) {
      background: rgba(var(--c-warning), 0.1);
    }
    &::-webkit-calendar-picker-indicator {
      opacity: 0;
      width: 30px;
      height: 100%;
      z-index: 1;
      cursor: pointer;
    }
  }
  .icon {
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    pointer-events: none;
  }
}
</style>

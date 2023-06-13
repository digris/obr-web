<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";

const props = defineProps<{
  code: string;
  isValid: boolean;
}>();

const emit = defineEmits(["input"]);

const el = ref<HTMLInputElement | null>(null);
const inputValue = ref(props.code);
const parseInput = (value: string) => {
  return value.toUpperCase().replace(/\s/g, "").substring(0, 8);
};
const handleInput = async (e: any) => {
  const value = parseInput(e.target.value);
  inputValue.value = value;
  emit("input", value);
};
const limitInput = computed(() => {
  return inputValue.value && inputValue.value.length >= 8 ? 8 : 100;
});
onMounted(() => {
  handleInput({
    target: {
      value: inputValue.value,
    },
  });
  el.value?.focus();
});
</script>

<template>
  <div class="code-input" :class="{ 'is-valid': isValid }">
    <div class="input-container">
      <i18n-t keypath="subscription.voucher.code" tag="label" for="ti-1299" />
      <input
        ref="el"
        id="ti-1299"
        class="input"
        @input="handleInput"
        :value="inputValue"
        :maxlength="limitInput"
        placeholder="Code: AB-CD-EF"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";

.code-input {
  @include form.default;

  .input-container {
    @include form.top-label;

    > label {
      &::after {
        content: ":";
      }
    }
  }

  .input {
    @include form.input;

    font-size: 200%;
    transition: background 200ms;
  }

  &.is-valid {
    .input {
      background: rgb(var(--c-success) / 10%);
      border-color: rgb(var(--c-success));
    }
  }
}
</style>

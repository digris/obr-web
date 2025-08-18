<script lang="ts" setup>
import { type Ref, computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";

import FlowSinglePayment from "./FlowSinglePayment.vue";

const AMOUNT_OPTIONS = [5, 10, 20, 50, 100, 200];

const props = defineProps<{
  currency: string;
}>();

const { t } = useI18n();

const emit = defineEmits<{
  (e: "success", response: object): void;
  (e: "step", step: string): void;
}>();

watch(
  // NOTE: ensure flow is reset on currency change
  () => props.currency,
  () => {
    setStep("amount");
  }
);

onMounted(async () => {
  setStep("amount");
});

const amount = ref(0);

const step = ref("amount"); // amount / payment

const customAmount: Ref<number | null> = ref<number | null>(null);

const options = computed(() => {
  return AMOUNT_OPTIONS.map((a) => {
    return {
      amount: a,
      isSelected: amount.value === a && customAmount.value === null,
    };
  });
});

const amountValid = computed(() => {
  return amount.value >= 1 && amount.value <= 5000;
});

const setAmount = (value: number) => {
  amount.value = value;
  customAmount.value = null;
};

const setStep = (value: string) => {
  step.value = value;
  emit("step", value);
};

watch(customAmount, (newValue) => {
  if (newValue !== null && newValue >= 1 && newValue <= 5000) {
    amount.value = newValue;
  } else {
    amount.value = 0;
  }
});
</script>

<template>
  <div v-if="step === 'amount'">
    <div class="options">
      <div
        @click.prevent="setAmount(option.amount)"
        :class="{ 'is-selected': option.isSelected }"
        v-for="(option, index) in options"
        :key="`single-amount-option-${index}`"
        class="option"
      >
        <span>{{ currency }}</span> <span>{{ option.amount }}</span>
      </div>
    </div>
    <div class="custom-amount">
      <input
        min="1"
        max="10000"
        type="number"
        :placeholder="t('donate.flow.single.customAmount')"
        :class="{ 'is-selected': typeof customAmount === 'number' && customAmount > 0 }"
        v-model="customAmount"
      />
    </div>
    <div class="actions">
      <button
        @click.prevent="setStep('payment')"
        class="action action--continue"
        :disabled="!amountValid"
      >
        <i18n-t keypath="donate.flow.continue" />
      </button>
    </div>
  </div>
  <div v-if="step === 'payment'">
    <div @click.prevent="setStep('amount')" class="navigate-back">
      <span>⇽ <i18n-t keypath="donate.flow.back" /></span>
    </div>
    <FlowSinglePayment
      @success="(response: object) => emit('success', response)"
      :amount="amount"
      :currency="currency"
    />
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/button";

.navigate-back {
  min-height: 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;

  .option {
    font-size: unset;
    color: rgb(var(--c-white));
    cursor: pointer;
    min-height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
    border-radius: 0.25rem;
    background: rgb(var(--c-white) / 15%);
    transition: background 200ms, border-radius 200ms;

    &:not(:disabled) {
      @include responsive.on-hover {
        background: rgb(var(--c-green) / 100%);
      }
    }

    &:hover {
      &:not(.is-selected) {
        border-radius: 1rem;
      }
    }

    &.is-selected {
      background: rgb(var(--c-green) / 100%);
      color: rgb(var(--c-white));
    }
  }
}

.custom-amount {
  margin-top: 1rem;

  > input {
    width: 100%;
    background: rgb(var(--c-light) / 5%);
    color: rgb(var(--c-dark));
    font-size: 1rem;
    outline: none;
    min-height: 2rem;
    border: 1px solid rgb(var(--c-white) / 20%);
    border-radius: 0.25rem;
    text-align: center;
    padding-left: 1rem;
    padding-right: 1rem;

    &::placeholder {
      color: rgb(var(--c-white) / 50%);
    }

    transition: border 200ms, background 200ms;

    &:focus {
      border-color: rgb(var(--c-green) / 100%);
      border-radius: 1rem;
    }

    &.is-selected {
      border-color: rgb(var(--c-green) / 100%);
      color: rgb(var(--c-white));
    }
  }
}

.actions {
  margin-top: 1rem;

  > button {
    @include button.default;

    font-size: unset;
    color: rgba(var(--c-white) / 100%);
    width: 100%;
    background: rgb(var(--c-green) / 100%);

    &:disabled {
      background: rgb(var(--c-white) / 20%);
      cursor: not-allowed;
    }

    &:not(:disabled) {
      @include responsive.on-hover {
        background: rgb(var(--c-green) / 90%);
      }
    }
  }
}
</style>

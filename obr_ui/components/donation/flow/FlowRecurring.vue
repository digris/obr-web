<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { APIClient } from "@/api/client";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

import FlowRecurringPayment from "./FlowRecurringPayment.vue";

const props = defineProps<{
  currency: string;
}>();

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

const step = ref("amount"); // amount / payment

const { user } = useAccount();
const route = useRoute();

const authenticate = () => {
  const event = {
    intent: "login",
    next: `${route.path}#donate:recurring`,
    // next: "/foo-bar/",
  };
  eventBus.emit("account:authenticate", event);
};

const options = ref([]);
const priceId = ref(null);
const option = computed(() => {
  return options.value.find((o) => o.priceId === priceId.value) || null;
});

const optionsDisplay = computed(() => {
  return options.value
    .filter((o) => o.currency === props.currency)
    .sort((a, b) => a.amount - b.amount) // <-- sort ascending
    .map((o) => {
      return {
        ...o,
        isSelected: priceId.value === o.priceId,
      };
    });
});

// initialize step and retrieve options (calls stripe API in backend)
onMounted(async () => {
  setStep("amount");
  const url = "/api/v1/donation/recurring/options/";
  const response = await APIClient.get(url);
  options.value = response.data;
});

const setPriceId = (value: string) => {
  console.debug("setPriceId", value);
  priceId.value = value;
};

const setStep = (value: string) => {
  step.value = value;
  emit("step", value);
};
</script>

<template>
  <div v-if="!user">
    <div class="notice notice--anonymous">
      <p>Want to donate monthly?</p>
      <p>
        Please log in or create an account first — this helps if you ever want to cancel your
        donation later. 😉
      </p>
    </div>
    <div class="actions">
      <button @click.prevent="authenticate" class="action action--continue">Sign in</button>
    </div>
  </div>
  <div v-else>
    <div v-if="step === 'amount'">
      <div class="options">
        <div
          @click.prevent="setPriceId(option.priceId)"
          :class="{ 'is-selected': option.isSelected }"
          v-for="(option, index) in optionsDisplay"
          :key="`single-amount-option-${index}`"
          class="option"
        >
          <span>{{ option.currency }}</span> <span>{{ option.amount }}</span>
        </div>
      </div>
      <div class="actions">
        <button
          @click.prevent="setStep('payment')"
          class="action action--continue"
          :disabled="!option"
        >
          Continue
        </button>
      </div>
    </div>
    <div v-if="option && step === 'payment'">
      <div @click.prevent="setStep('amount')" class="navigate-back">
        <span>⇽ Back</span>
      </div>
      <FlowRecurringPayment
        @success="(response: object) => emit('success', response)"
        :price-id="priceId"
        :amount="option.amount"
        :currency="currency"
      />
    </div>
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

.notice {
  margin-bottom: 4rem;

  > p {
    &:not(:last-child) {
      margin-bottom: 0.5rem;
    }
  }
}

.options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  min-height: 128px;
  align-items: center;

  .option {
    font-size: unset;
    color: rgb(var(--c-white));
    cursor: pointer;
    min-height: 3rem;
    max-height: 3rem;
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
        border-radius: 1.5rem;
      }
    }

    &.is-selected {
      background: rgb(var(--c-green) / 100%);
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

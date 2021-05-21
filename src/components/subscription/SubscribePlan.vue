<script lang="ts">
import {
  computed,
  defineComponent,
  onMounted,
  ref,
} from 'vue';
import { loadStripe } from '@stripe/stripe-js';
import settings from '@/settings';
import AsyncButton from '@/components/ui/button/AsyncButton.vue';
import APIErrors from '@/components/ui/error/APIErrors.vue';
import { getPlanOptions, createStripeCheckoutSession } from '@/api/subscription';
import Datetime from '@/components/ui/Datetime.vue';
import Money from '@/components/ui/Money.vue';

const { STRIPE_PUBLISHABLE_KEY } = settings;
const stripePromise = loadStripe(STRIPE_PUBLISHABLE_KEY);

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    Datetime,
    Money,
  },
  setup() {
    const errors = ref<Array<String>>([]);
    const message = ref(null);
    const selectedKey = ref(null);
    const options = ref([]);
    const fetchOptions = async () => {
      errors.value = [];
      try {
        const response = await getPlanOptions();
        message.value = response.message;
        options.value = response.options;
        if (response.options.length) {
          selectedKey.value = response.options[0].sku;
        }
      } catch (err: any) {
        errors.value = [err.response];
      }
    };
    const selectOption = (option: any) => {
      selectedKey.value = option.sku;
    };
    const selectedOption = computed(() => {
      if (!selectedKey.value) {
        return null;
      }
      return options.value.find((o: any) => o.sku === selectedKey.value);
    });
    const startStripePayment = async () => {
      const stripe = await stripePromise;
      // @ts-ignore
      const response = await createStripeCheckoutSession(selectedOption.value.sku);
      console.debug('response', response);
      const sessionId = response.id;
      console.debug('sessionId', sessionId);
      // @ts-ignore
      const result = await stripe.redirectToCheckout({
        sessionId,
      });
      if (result.error) {
        // If `redirectToCheckout` fails due to a browser or network
        // error, display the localized error message to your customer
        // using `result.error.message`.
        console.error(result.error);
      }
    };
    const startPayment = async (provider: string) => {
      errors.value = [];
      if (provider === 'stripe') {
        await startStripePayment();
      }
    };

    onMounted(() => {
      fetchOptions();
    });
    return {
      message,
      options,
      selectedOption,
      selectOption,
      errors,
      startPayment,
    };
  },
});
</script>

<template>
  <div
    class="subscribe-plan"
  >
    <section
      class="section info"
    >
      <div>
        <p
          class="message"
          v-text="message"
        />
        <div
          class="options"
        >
          <div
            v-for="(option, index) in options"
            @click="selectOption(option)"
            :key="`options-${index}-${option.sku}`"
            class="option"
            :class="{'is-selected': option.sku === selectedOption.sku}"
          >
            <div
              class="num-days"
            >
              {{ option.numDays }} days
            </div>
            <div
              class="price"
            >
              <Money
                :value="option.price"
                :include-currency="(false)"
              />
            </div>
            <div
              class="title"
            >
              {{ option.title }}
            </div>
            <div
              class="until-date"
            >
              until
              <Datetime
                :value="option.untilDate"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
    <section
      v-if="selectedOption"
      class="section total"
    >
      <div
        class="title"
      >
        TOTAL:
      </div>
      <div
        class="price"
      >
        <Money
          :value="selectedOption.price"
        />
      </div>
    </section>
    <section
      v-if="errors"
      class="section errors"
    >
      <APIErrors
        :errors="errors"
      />
    </section>
    <section
      class="section actions"
    >
      <AsyncButton
        class="button"
        @click.prevent="startPayment('stripe')"
      >
        (CC) Complete Order
      </AsyncButton>
      <AsyncButton
        class="button"
        @click.prevent="startPayment('paypal')"
      >
        (PP) Complete Order
      </AsyncButton>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
@use "@/style/elements/button";
.section {
  @include section.default;
  &.info {
    .message {
      padding: 1rem 0;
    }
    .details {
      font-size: 150%;
    }
  }
}
@mixin options {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: 1fr 1fr 1fr 1fr;
}
@mixin option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: rgb(var(--c-gray-50));
  cursor: pointer;
  transition: background 100ms;
  &:hover {
    background: rgba(var(--c-selected), 0.5);
  }
  &.is-selected {
    background: rgb(var(--c-selected));
  }
  .num-days {
    padding: 0.5rem 0;
    opacity: 0.75;
  }
  .price {
    font-size: 200%;
  }
  .title {
    padding: 0.5rem 0;
    font-size: 120%;
  }
  .until-date {
    padding: 0.5rem 0;
    opacity: 0.75;
  }
}
.options {
  @include options;
  .option {
    @include option;
  }
}
.total {
  display: flex;
  padding: 0.5rem 0.5rem;
  font-weight: 800;
  border-top: 3px solid rgb(var(--c-black));
  border-bottom: 1px solid rgb(var(--c-black));
  .title {
    flex-grow: 1;
  }
}
.actions {
  display: flex;
  align-items: center;
  justify-content: center;
  .button {
    @include button.default(3rem);
    min-width: 200px;
    margin-right: 0.5rem;
    margin-left: 0.5rem;
  }
}
</style>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import { loadStripe } from "@stripe/stripe-js";
import settings from "@/settings";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import { getPlanOptions, createStripeCheckoutSession } from "@/api/subscription";
import Datetime from "@/components/ui/date/Datetime.vue";
import Money from "@/components/ui/Money.vue";

const { STRIPE_PUBLISHABLE_KEY } = settings;
// const stripePromise = loadStripe(STRIPE_PUBLISHABLE_KEY);

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    Datetime,
    Money,
  },
  props: {
    next: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const errors = ref<Array<string>>([]);
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
    const stripePromise = loadStripe(STRIPE_PUBLISHABLE_KEY);
    const startStripePayment = async () => {
      const stripe = await stripePromise;
      // @ts-ignore
      const response = await createStripeCheckoutSession(selectedOption.value.sku, props.next);
      // if (response) {
      //   throw new Error('foo');
      // }
      console.debug("response", response);
      const sessionId = response.id;
      console.debug("sessionId", sessionId);
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
      if (provider === "stripe") {
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
  <div class="subscribe-plan">
    <section class="section info">
      <div>
        <p class="message" v-text="message" />
        <div class="options">
          <div
            v-for="(option, index) in options"
            @click="selectOption(option)"
            :key="`options-${index}-${option.sku}`"
            class="option"
            :class="{ 'is-selected': option.sku === selectedOption.sku }"
          >
            <div class="price">
              <Money :value="option.price" :include-currency="true" />
            </div>
            <div class="separator" />
            <div class="title">
              {{ option.title }}
            </div>
            <div class="until-date">
              Gültig bis am
              <Datetime :value="option.untilDate" :display-time="false" />
            </div>
          </div>
        </div>
      </div>
    </section>
    <section v-if="selectedOption" class="section total">
      <div class="title">Total inkl. aller Steuren und Gebühren</div>
      <div class="price">
        <Money :value="selectedOption.price" />
      </div>
    </section>
    <section v-if="errors" class="section errors">
      <APIErrors :errors="errors" />
    </section>
    <section class="section actions">
      <AsyncButton class="button" @click.prevent="startPayment('stripe')">
        Jetzt Bezahlen
      </AsyncButton>
      <!--
      <AsyncButton
        class="button"
        @click.prevent="startPayment('paypal')"
      >
        (PP) Complete Order
      </AsyncButton>
      -->
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/base/typo";
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
  grid-template-columns: 1fr 1fr 1fr;
  @include responsive.bp-medium {
    grid-template-columns: unset;
  }
}
@mixin option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: rgb(var(--c-white));
  box-shadow: 0 0 3px rgba(var(--c-black), 0.33);
  cursor: pointer;
  transition: background 100ms;
  &:hover {
    background: rgb(var(--c-gray-100));
  }
  &.is-selected {
    color: rgb(var(--c-white));
    background: rgb(var(--c-green));
  }
  .price {
    font-size: 200%;
  }
  .separator {
    width: 100%;
    height: 1px;
    margin: 1rem 0;
    background: rgb(var(--c-gray-100));
  }
  .title {
    padding: 0;
  }
  .until-date {
    padding: 0;
  }
  //@include responsive.bp-medium {
  //  padding: 0.25rem 0.5rem 0.5rem;
  //  .price {
  //    font-size: 120%;
  //  }
  //  .separator {
  //    display: none;
  //  }
  //  .title {
  //    @include typo.small;
  //    padding-top: 0.25rem;
  //  }
  //  .until-date {
  //    @include typo.small;
  //  }
  //}
  @include responsive.bp-medium {
    padding: 0.5rem 1rem 0.5rem 0.5rem;
    display: grid;
    grid-gap: 0.25rem;
    grid-template-areas:
      "title price"
      "date  price";
    .separator {
      display: none;
    }
    .price {
      grid-area: price;
      font-size: 120%;
      justify-self: end;
    }
    .title {
      grid-area: title;
    }
    .until-date {
      grid-area: date;
      @include typo.small;
    }
  }
}
.options {
  @include options;
  .option {
    @include option;
  }
}
.total {
  padding: 0.5rem 0.5rem;
  .title {
    margin-bottom: 0.5rem;
  }
  .price {
    @include typo.large;
    @include typo.bold;
    @include responsive.bp-medium {
      color: rgb(var(--c-green));
      font-size: 150%;
    }
  }
}
.actions {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  .button {
    @include button.default(3rem);
    min-width: 33%;
    margin-right: 0.5rem;
    margin-left: 0.5rem;
    @include responsive.bp-medium {
      width: 100%;
    }
  }
}
</style>

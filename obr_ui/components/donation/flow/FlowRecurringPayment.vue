<script lang="ts" setup>
import { type Ref, onMounted, ref } from "vue";
import { loadStripe } from "@stripe/stripe-js/pure";

import { APIClient } from "@/api/client";
import Spinner from "@/components/ui/loading/Spinner.vue";
import settings from "@/settings";

const { STRIPE_PUBLISHABLE_KEY } = settings;

const props = defineProps<{
  priceId: string;
  amount: number;
  currency: string;
}>();

const emit = defineEmits<{
  (e: "success", response: object): void;
}>();

const errors = ref<string[]>([]);

class PaymentFlow {
  private baseUrl = "/api/v1/donation/";
  private stripe: any = null;
  private elements: any = null;
  private donationUid: string | null = null;
  private clientSecret: string | null = null;

  constructor(
    private emitFn: ReturnType<typeof defineEmits>,
    private errorsRef: Ref<string[]>,
    private formEl: HTMLFormElement,
    private priceId: string,
    private amount: number,
    private currency: string
  ) {}

  public async init(): Promise<void> {
    const url = `${this.baseUrl}create/`;

    try {
      const response = await APIClient.post(url, {
        kind: "recurring",
        priceId: this.priceId,
        amount: this.amount,
        currency: this.currency,
      });
      this.donationUid = response.data.uid;
      this.clientSecret = response.data.clientSecret;
    } catch (err) {
      console.error("Error initializing payment flow:", err);
      this.errorsRef.value.push(err?.response?.data?.message || err?.message || "Unknown error");
      return;
    }

    this.stripe = await loadStripe(STRIPE_PUBLISHABLE_KEY);

    if (!this.stripe) throw new Error("Stripe failed to load");

    this.elements = this.stripe.elements({
      clientSecret: this.clientSecret,
      appearance: {
        theme: "night",
        variables: {
          colorPrimary: "#009050",
          colorBackground: "#222222",
          colorText: "#ffffff",
          colorDanger: "#df1b41",
          tabLogoColor: "dark",
          fontSizeBase: "16px",
          fontFamily: "IBM Plex Sans, Helvetica Neue, system-ui, sans-serif",
          spacingUnit: "3px",
          borderRadius: "4px",
          gridRowSpacing: "16px",
        },
      },
    });

    await this.mountExpressCheckout();
    await this.mountCardPayment();
  }

  private async mountExpressCheckout(): Promise<void> {
    const expressEl = this.elements.create("expressCheckout", {
      buttonHeight: 44,
      buttonTheme: {
        applePay: "white",
        googlePay: "black",
        paypal: "black",
        klarna: "dark",
      },
      buttonType: {
        applePay: "donate",
        googlePay: "donate",
        paypal: "paypal",
        klarna: "continue",
      },
    });

    expressEl.on("ready", async (event) => {
      console.debug("expressEl:ready", event);
      this.formEl.querySelector(".express-checkout")?.classList.remove("is-loading");
    });

    expressEl.on("click", async (event) => {
      // NOTE: here we get the customer contact information
      //       maybe use it in case of anonymous user...
      console.debug("expressEl:click", event);
      event.resolve({
        emailRequired: true,
      });
    });

    expressEl.on("confirm", async () => {
      await this.confirmPayment();
    });

    expressEl.mount("#express-checkout");
  }

  private async mountCardPayment(): Promise<void> {
    const cardEl = this.elements.create("payment", {
      layout: "tabs",
      wallets: {
        applePay: "auto",
        googlePay: "auto",
        link: "never",
      },
    });

    cardEl.mount("#payment");

    cardEl.on("ready", async (event) => {
      console.debug("cardEl:ready", event);
      this.formEl.querySelector(".payment")?.classList.remove("is-loading");
    });
  }

  public async confirmPayment(): Promise<void> {
    if (!this.stripe || !this.elements || !this.clientSecret) return;

    this.errorsRef.value = [];

    await this.elements.submit();

    const next = encodeURIComponent(document.location.pathname);

    const result = await this.stripe.confirmPayment({
      elements: this.elements,
      clientSecret: this.clientSecret,
      confirmParams: {
        return_url: `${window.location.origin}${this.baseUrl}return/?next=${next}`,
      },
      redirect: "if_required",
    });

    if (result.error) {
      console.error("payment:failed", result.error);
      this.errorsRef.value.push(result.error?.message || "Unknown error");
    } else {
      console.debug("payment:completed", result);
      const paymentIntentId = result.paymentIntent.id;
      const url = `${this.baseUrl}${paymentIntentId}/finalize/`;
      const response = await APIClient.post(url, {
        uid: this.donationUid,
      });
      console.debug("payment:finalized", response);
      this.emitFn("success", response.data);
    }
  }
}

const formEl = ref<HTMLFormElement | null>(null);
let flow: PaymentFlow;

onMounted(async () => {
  flow = new PaymentFlow(emit, errors, formEl.value, props.priceId, props.amount, props.currency);
  await flow.init();
});

const submitPayment = async () => {
  if (flow) await flow.confirmPayment();
};
</script>

<template>
  <form @submit.prevent="submitPayment" class="payment-form" ref="formEl">
    <div class="express-checkout is-loading">
      <div id="express-checkout" />
    </div>
    <div class="payment is-loading">
      <div class="loading-placeholder">
        <Spinner :scale="2" color-var="--c-white" />
      </div>
      <div id="payment" />
    </div>
    <div v-if="errors.length" class="errors">
      <p v-for="(error, index) in errors" :key="`error-${index}`" class="error">{{ error }}</p>
    </div>
    <div class="actions">
      <button>
        <span>Monatlich</span>
        <span v-text="currency" />
        <span v-text="amount" />
        <span>spenden!</span>
      </button>
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/button";

.loading-placeholder {
  position: absolute;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--c-white) / 10%);
  border-radius: 0.35rem;
}

.payment-form {
  > .express-checkout {
    margin-bottom: 1rem;
    min-height: 64px;
    position: relative;

    &.is-loading {
      height: 64px;
      overflow: hidden;
    }
  }

  > .payment {
    margin-bottom: 1rem;
    min-height: 260px;
    position: relative;

    &.is-loading {
      height: 260px;
      overflow: hidden;
    }

    /* stylelint-disable-next-line selector-class-pattern */
    &:has(.StripeElement) {
      .loading-placeholder {
        display: none;
      }
    }
  }

  > .errors {
    @include typo.default;
    @include typo.light;

    color: rgba(var(--c-red) / 100%);
    background: rgba(var(--c-red) / 20%);
    padding: 0.5rem;
    border-radius: 0.35rem;
  }

  > .actions {
    margin-top: 2rem;

    button {
      @include button.default;

      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.25rem;
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
}
</style>

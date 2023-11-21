<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import type { AxiosError } from "axios";

import { getVoucher, redeemVoucher } from "@/api/subscription";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import Datetime from "@/components/ui/date/Datetime.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import ModalPanel from "@/components/ui/panel/ModalPanel.vue";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";
import type { Voucher } from "@/typings";

const codeRegex = new RegExp("^([A-Z]{2})-?([A-Z]{2})-?([A-Z]{2})$");

export default defineComponent({
  components: {
    ModalPanel,
    ApiErrors,
    AsyncButton,
    Datetime,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const { user, loadUser } = useAccount();
    const errors = ref<Array<string | AxiosError>>([]);
    const voucher = ref<Voucher | null>(null);
    const isValid = computed(() => !!voucher.value);
    const code = computed(() => {
      if (!route.hash.startsWith("#")) {
        return "";
      }
      const hashValue = route.hash.replace("#", "");
      return codeRegex.test(hashValue) ? hashValue : null;
    });
    const fetchVoucher = async (codeValue: string) => {
      voucher.value = null;
      errors.value = [];
      try {
        voucher.value = await getVoucher(codeValue);
      } catch (err: unknown) {
        const error = err as AxiosError;
        errors.value = [error];
      }
    };
    const redeem = async () => {
      errors.value = [];
      if (!code.value) {
        return;
      }
      try {
        const response = await redeemVoucher(code.value);
        console.debug("redeem voucher", response);
        await loadUser();
        await router.replace(route.path);
      } catch (err: unknown) {
        const error = err as AxiosError;
        errors.value = [error];
        throw err;
      }
    };
    const authenticateAndRedeem = () => {
      const event = {
        intent: "login",
        next: `${route.path}#${code.value}`,
      };
      eventBus.emit("account:authenticate", event);
    };
    const closePanel = () => {
      router.push(route.path);
    };
    watch(
      () => code.value,
      async () => {
        if (!code.value) {
          return;
        }
        if (codeRegex.test(code.value)) {
          await fetchVoucher(code.value);
        } else {
          voucher.value = null;
        }
      }
    );
    return {
      user,
      code,
      voucher,
      errors,
      isValid,
      closePanel,
      authenticateAndRedeem,
      redeem,
    };
  },
});
</script>

<template>
  <ModalPanel :is-visible="!!code" @close="closePanel">
    <div class="claim-voucher">
      <section class="code">
        <div>
          <p v-text="`Code: ${code}`" />
        </div>
      </section>
      <section v-if="errors && errors.length" class="error">
        <i18n-t keypath="subscription.voucher.invalidCode" tag="p" class="error__notes" />
        <ApiErrors :errors="errors" />
      </section>
      <section v-if="voucher" class="voucher">
        <div class="voucher__details">
          <p>
            <i18n-t keypath="subscription.validNumDays" :plural="voucher.numDays" />
          </p>
          <i18n-t keypath="subscription.validUntilDate" tag="p">
            <Datetime v-if="voucher.untilDate" :value="voucher.untilDate" :display-time="false" />
          </i18n-t>
        </div>
      </section>
      <section class="actions">
        <AsyncButton v-if="user" class="button" :disabled="!isValid" @click.prevent="redeem">
          <i18n-t keypath="subscription.voucher.redeem" />
        </AsyncButton>
        <AsyncButton
          v-else
          class="button"
          :disabled="!isValid"
          @click.prevent="authenticateAndRedeem"
        >
          <i18n-t keypath="subscription.voucher.authenticateAndRedeem" />
        </AsyncButton>
      </section>
      <pre
        v-if="false"
        v-text="{
          user,
          code,
          voucher,
          isValid,
        }"
      />
    </div>
  </ModalPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/button";

.claim-voucher {
  .code {
    @include typo.x-large;

    padding: 0 0 1rem;
  }

  .error {
    padding: 0 0 1rem;

    &__notes {
      @include typo.large;

      padding: 0 0 1rem;
    }
  }

  .voucher {
    padding: 0 0 1rem;

    &__details {
      @include typo.large;
    }
  }

  .actions {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 1rem 0 0;

    .button {
      @include button.default(3rem);

      min-width: 33%;

      @include responsive.bp-medium {
        width: 100%;
      }
    }
  }
}
</style>

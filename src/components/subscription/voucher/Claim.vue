<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { getVoucher, redeemVoucher } from "@/api/subscription";

import eventBus from "@/eventBus";

import ModalPanel from "@/components/ui/panel/ModalPanel.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import Datetime from "@/components/ui/date/Datetime.vue";

const codeRegex = new RegExp("^([A-Z]{2})-?([A-Z]{2})-?([A-Z]{2})$");

export default defineComponent({
  components: {
    ModalPanel,
    APIErrors,
    AsyncButton,
    Datetime,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    const user = computed(() => store.getters["account/user"]);
    const errors = ref<Array<string>>([]);
    const voucher = ref(null);
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
      } catch (err: any) {
        errors.value = [err.response];
      }
    };
    const redeem = async () => {
      errors.value = [];
      try {
        const response = await redeemVoucher(code.value);
        console.debug(response);
        await store.dispatch("account/getUser");
        await router.replace(route.path);
      } catch (err: any) {
        console.warn(err);
        console.warn(err.response);
        errors.value = [err.response];
        throw err;
      }
    };
    const authenticateAndRedeem = () => {
      const event = {
        intent: "login",
        next: `${route.path}#${code.value}`,
      };
      console.debug("Authenticate", event);
      eventBus.emit("account:authenticate", event);
    };
    const closePanel = () => {
      router.push(route.path);
    };
    watch(
      () => code.value,
      async () => {
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
        <p class="error__notes">Ungültiger Gutschein-Code.</p>
        <APIErrors :errors="errors" />
      </section>
      <section v-if="voucher" class="voucher">
        <div class="voucher__details">
          <p>+ {{ voucher.numDays }} Tage</p>
          <p>
            Guthaben bis am
            <Datetime :value="voucher.untilDate" :display-time="false" />
          </p>
        </div>
      </section>
      <section class="actions">
        <div v-if="user">
          <AsyncButton class="button" :disabled="!isValid" @click.prevent="redeem">
            Jetzt Einlösen
          </AsyncButton>
        </div>
        <div v-else>
          <AsyncButton class="button" :disabled="!isValid" @click.prevent="authenticateAndRedeem">
            Anmelden und einlösen
          </AsyncButton>
        </div>
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
    }
  }
}
</style>

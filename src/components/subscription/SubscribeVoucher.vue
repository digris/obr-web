<script lang="ts">
import {
  defineComponent,
  computed,
  ref,
} from 'vue';
import { useStore } from 'vuex';
import { debounce } from 'lodash-es';
import AsyncButton from '@/components/ui/button/AsyncButton.vue';
import APIErrors from '@/components/ui/error/APIErrors.vue';
import { getVoucher, redeemVoucher } from '@/api/subscription';
import Datetime from '@/components/ui/date/Datetime.vue';
import CodeInput from './voucher/CodeInput.vue';

const codeRegex = new RegExp('^([A-Z]{2})-?([A-Z]{2})-?([A-Z]{2})$');

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    Datetime,
    CodeInput,
  },
  props: {
    code: {
      type: String,
      default: '',
    },
    next: {
      type: String,
      default: null,
    },
  },
  emits: [
    'subscriptionExtended',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const errors = ref<Array<string>>([]);
    const codeInput = ref(props.code);
    const voucher = ref(null);
    const isValid = computed(() => !!voucher.value);

    const fetchVoucher = async (code: string) => {
      errors.value = [];
      try {
        voucher.value = await getVoucher(code);
      } catch (err: any) {
        errors.value = [err.response];
      }
    };

    const handleCodeInput = debounce(async (value: string) => {
      if (codeRegex.test(value)) {
        await fetchVoucher(value);
      } else {
        voucher.value = null;
      }
    }, 200);

    const redeem = async () => {
      if (!voucher.value) {
        return;
      }
      // @ts-ignore
      const code = voucher.value?.code;
      if (!codeRegex.test(code)) {
        console.warn('invalid code', code);
        return;
      }
      errors.value = [];
      try {
        const response = await redeemVoucher(code);
        console.debug(response);
        await store.dispatch('account/getUser');
        emit('subscriptionExtended');
      } catch (err: any) {
        console.warn(err);
        console.warn(err.response);
        errors.value = [err.response];
        throw err;
      }
    };
    return {
      errors,
      codeInput,
      handleCodeInput,
      voucher,
      isValid,
      redeem,
    };
  },
});
</script>

<template>
  <div
    class="subscribe-voucher"
  >
    <!--
    <section
      class="section info"
    >
      <p>.</p>
    </section>
    -->
    <section
      class="section input"
    >
      <div>
        <CodeInput
          :code="codeInput"
          :valid="isValid"
          @input="handleCodeInput"
        />
      </div>
      <div>
        <pre
          v-text="voucher"
          class="_debug"
        ></pre>
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
      v-if="voucher"
      class="section voucher"
    >
      <div>
        <p>
          + {{ voucher.numDays }} Tage
        </p>
        <p>
          Guthaben bis am
          <Datetime
            :value="voucher.untilDate"
            :display-time="(false)"
          />
        </p>
      </div>
    </section>
    <section
      class="section actions"
    >
      <AsyncButton
        class="button"
        :disabled="(!isValid)"
        @click.prevent="redeem"
      >
        Jetzt Einlösen
      </AsyncButton>
    </section>
  </div>
</template>

<style lang="scss" scoped>
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
  &.voucher {
    @include typo.large;
    padding-left: 0.5rem;
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
  }
}
</style>

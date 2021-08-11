<script lang="ts">
import { debounce } from 'lodash-es';
import { defineComponent, ref } from 'vue';
// import { useStore } from 'vuex';

import AsyncButton from '@/components/ui/button/AsyncButton.vue';
import APIErrors from '@/components/ui/error/APIErrors.vue';
import TokenInput from '@/components/account/TokenInput.vue';

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    TokenInput,
  },
  emits: [
    'emailSent',
  ],
  setup() {
    // const store = useStore();
    const email = ref('');
    const token = ref('');
    const tokenValid = ref(false);
    const errors = ref<Array<string>>([]);

    const handleTokenInput = debounce(async (e: any) => {
      const { value } = e.target;
      errors.value = [];
      console.debug('value', value);
    }, 200);

    const submitForm = async () => {
      console.debug('submit form');
    };

    return {
      email,
      token,
      tokenValid,
      errors,
      handleTokenInput,
      submitForm,
    };
  },
});
</script>

<template>
  <div>
    <p
      class="lead"
    >
      Eine E-Mail mit einem Login-Code wurde an {{ email }} geschickt.<br>
      Falls du kein E-Mail erhalten hast, prüfe dein Spam Ordner.<br>
      E-Mail erneut senden
    </p>
  </div>
  <form
    class="form"
  >
    <TokenInput
      ref="tokenInputRef"
      :token="token"
      @input="token = $event"
    />
    <div
      class="form-errors"
      v-if="errors.length"
    >
      <APIErrors
        :errors="errors"
      />
    </div>
    <div
      class="input-container submit"
    >
      <AsyncButton
        class="button"
        @click.prevent="submitForm"
        :disabled="(!tokenValid)"
      >
        Anmelden
      </AsyncButton>
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/form";
.form {
  @include form.default;
  display: flex;
  flex-direction: column;
  .input-container {
    @include form.float-label;
    width: 100%;
    .input {
      @include typo.large;
    }
    &.submit {
      padding-top: 2rem;
      .button {
        max-width: 33%;
      }
    }
  }
  .token-input {
    display: flex;
    flex-direction: column;
    //align-items: center;
    //justify-content: center;
    padding: 1rem 0;
  }
}
.lead {
  @include typo.large;
  a {
    text-decoration: underline;
    cursor: pointer;
  }
}
.form-messages,
.form-errors {
  margin: 1rem 0;
}
</style>

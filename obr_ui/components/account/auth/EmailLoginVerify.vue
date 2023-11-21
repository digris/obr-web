<script lang="ts" setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { whenever } from "@vueuse/core";
import type { AxiosError } from "axios";

import TokenInput from "@/components/account/auth/TokenInput.vue";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import { useAccount } from "@/composables/account";

const tokenRegex = new RegExp("^([A-Z0-9]{3})-?([A-Z0-9]{3})$");

const props = defineProps<{
  email: string;
}>();

const emit = defineEmits(["reset"]);

const { t } = useI18n();
const { loadUser, loginUserByToken } = useAccount();
const token = ref("");
const tokenValid = ref(false);
const errors = ref<Array<string | AxiosError>>([]);

const handleTokenInput = async (value: string) => {
  token.value = value;
  tokenValid.value = tokenRegex.test(value);
  errors.value = [];
};

const submitForm = async () => {
  if (!tokenValid.value) {
    return;
  }
  errors.value = [];
  const credentials = {
    email: props.email,
    token: token.value,
  };
  try {
    const { created } = await loginUserByToken(credentials);
    await loadUser();
    if (created) {
      document.location = "/account/";
    } else {
      document.location.reload();
    }
  } catch (err: unknown) {
    const error = err as AxiosError;
    errors.value = [error];
    throw error;
  }
};

// auto-submit form when token (format) is valid
whenever(tokenValid, submitForm);

const reset = async () => {
  emit("reset");
};
</script>

<template>
  <div>
    <p class="lead">
      <i18n-t keypath="account.auth.loginEmailSent.title" tag="div" class="title">
        <em v-text="email" />
      </i18n-t>
      <i18n-t keypath="account.auth.loginEmailSent.note" tag="div" class="note" />
      <i18n-t @click.prevent="reset" keypath="account.auth.loginEmailSendAgain" tag="a" />
    </p>
    <form class="form" @submit.prevent="submitForm">
      <TokenInput ref="tokenInputRef" @input="handleTokenInput" />
      <div class="form-errors" v-if="errors.length">
        <ApiErrors :errors="errors" />
      </div>
      <div class="input-container submit">
        <AsyncButton
          class="button"
          @click.prevent="submitForm"
          :disabled="!tokenValid"
          v-text="t('account.auth.login')"
        />
      </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/form";

.form {
  @include form.default;

  display: flex;
  flex-direction: column;

  .input-container {
    width: 100%;

    .input {
      @include typo.large;
    }

    &.submit {
      padding-top: 2rem;

      .button {
        max-width: 33%;

        @include responsive.bp-medium {
          max-width: unset;
        }
      }
    }
  }

  .token-input {
    display: flex;
    flex-direction: column;
    padding: 1rem 0;
  }
}

.lead {
  .title {
    @include typo.large;
  }

  .note {
    margin-top: 1rem;
  }

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

<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";
import { whenever } from "@vueuse/core";
import * as EmailValidator from "email-validator";
import { debounce } from "lodash-es";

import { checkLoginEmail, sendLoginEmail } from "@/api/account";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import Message from "@/components/ui/Message.vue";
import { useAccount } from "@/composables/account";

export enum Flow {
  Password = "password",
  Token = "token",
  Register = "register",
}

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    Message,
  },
  emits: ["emailSent"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { loginUser } = useAccount();
    const email = ref("");
    const password = ref("");
    const emailValid = ref(false);
    const emailExists = ref(false);
    const promptPassword = ref(false);
    const buttonText = ref(t("account.auth.login"));
    const message = ref({});
    const errors = ref<Array<string>>([]);
    const flow = computed(() => {
      if (emailExists.value && promptPassword.value) {
        return Flow.Password;
      }
      if (emailExists.value) {
        return Flow.Token;
      }
      return Flow.Register;
    });
    const updateAccount = (account: any | null) => {
      message.value = "";
      if (account && account.uid) {
        emailExists.value = true;
        if (account.hasUsablePassword) {
          promptPassword.value = true;
          buttonText.value = t("account.auth.login");
        } else {
          message.value = {
            level: "info",
            body: t("account.auth.accountExists"),
          };
          buttonText.value = t("account.auth.sendToken");
        }
      } else {
        emailExists.value = false;
        promptPassword.value = false;
        buttonText.value = t("account.auth.register");
      }
    };
    const handleEmailInput = debounce(async (e: any) => {
      const { value } = e.target;
      errors.value = [];
      emailExists.value = false;
      promptPassword.value = false;
      if (EmailValidator.validate(value)) {
        emailValid.value = true;
        try {
          const account = await checkLoginEmail(value);
          updateAccount(account);
        } catch (err: any) {
          console.warn(err);
          errors.value = [err.response];
          // throw err;
        }
      } else {
        emailValid.value = false;
        buttonText.value = t("account.auth.login");
      }
    }, 200);
    const submitEmailLogin = async () => {
      message.value = {};
      errors.value = [];
      try {
        const response = await sendLoginEmail(email.value);
        emit("emailSent", response.email);
      } catch (err: any) {
        console.warn(err);
        errors.value = [err.response];
      }
    };
    const submitPasswordLogin = async () => {
      message.value = {};
      errors.value = [];
      const credentials = {
        email: email.value,
        password: password.value,
      };
      errors.value = [];
      try {
        await loginUser(credentials);
        document.location.reload();
      } catch (err) {
        console.warn(err);
        errors.value = [err.response];
      }
    };
    const submitForm = async () => {
      message.value = {};
      errors.value = [];
      if (flow.value === Flow.Register || flow.value === Flow.Token) {
        await submitEmailLogin();
      }
      if (flow.value === Flow.Password) {
        await submitPasswordLogin();
      }
    };
    const resetPassword = async () => {
      await submitEmailLogin();
    };

    // auto-submit form in case of existing account
    whenever(emailExists, async () => {
      if (!promptPassword.value) {
        await submitForm();
      }
    });

    return {
      flow,
      email,
      emailValid,
      password,
      emailExists,
      promptPassword,
      buttonText,
      message,
      errors,
      handleEmailInput,
      submitForm,
      resetPassword,
    };
  },
});
</script>

<template>
  <form class="form" @submit.prevent="submitForm">
    <div class="input-container">
      <i18n-t keypath="account.auth.usingEmail" tag="label" for="email-1625" />
      <input
        @keyup="handleEmailInput"
        class="input"
        v-model="email"
        required
        id="email-1625"
        name="email"
        type="email"
        placeholder="E-Mail"
        autocomplete="email"
      />
    </div>
    <div v-if="flow === 'password'" class="input-container">
      <i18n-t keypath="account.auth.password" tag="label" for="password-1625" />
      <input
        class="input"
        v-model="password"
        required
        id="password-1625"
        name="password"
        type="password"
        placeholder="Password"
        autocomplete="current-password"
      />
      <p class="help">
        <i18n-t keypath="account.auth.forgotPassword" tag="span" />
        <i18n-t @click.prevent="resetPassword" keypath="account.auth.resetPassword" tag="a" />
      </p>
    </div>
    <div class="form-messages" v-if="message && message.body">
      <Message :level="message.level" :body="message.body" />
    </div>
    <div class="form-errors" v-if="errors.length">
      <APIErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton
        class="button"
        @click.prevent="submitForm"
        :disabled="!emailValid"
        v-text="buttonText"
      />
    </div>
  </form>
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
    @include form.top-label;

    width: 100%;

    > label {
      &::after {
        content: ":";
      }
    }

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

    .help {
      > span {
        padding-right: 0.5rem;
      }

      @include responsive.bp-medium {
        @include typo.small;

        padding-top: 1rem;
        flex-direction: column;
        align-items: start;
        white-space: unset;
      }
    }
  }
}

.form-messages,
.form-errors {
  margin: 1rem 0;
}
</style>

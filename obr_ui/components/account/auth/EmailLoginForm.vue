<script lang="ts" setup>
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { whenever } from "@vueuse/core";
import * as EmailValidator from "email-validator";
import { debounce } from "lodash-es";
import type { AxiosError } from "axios";

import { checkLoginEmail, sendLoginEmail } from "@/api/account";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import Message from "@/components/ui/Message.vue";
import { useAccount } from "@/composables/account";

// import type {UiMessage} from "@/types.d";

enum Flow {
  Password = "password",
  Token = "token",
  Register = "register",
}

const props = defineProps<{
  next: string;
}>();

const emit = defineEmits(["emailSent"]);

const { t } = useI18n();
const router = useRouter();
const { loadUser, loginUser } = useAccount();
const email = ref("");
const password = ref("");
const emailValid = ref(false);
const emailExists = ref(false);
const promptPassword = ref(false);
const buttonText = ref(t("account.auth.login"));
const message = ref({});
const errors = ref<Array<string | AxiosError>>([]);
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
  message.value = {};
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
const handleEmailChanged = debounce(async (value: string) => {
  errors.value = [];
  emailExists.value = false;
  promptPassword.value = false;
  if (EmailValidator.validate(value)) {
    emailValid.value = true;
    try {
      const account = await checkLoginEmail(value);
      updateAccount(account);
    } catch (err: unknown) {
      const error = err as AxiosError;
      errors.value = [error];
    }
  } else {
    emailValid.value = false;
    buttonText.value = t("account.auth.login");
  }
}, 200);
/*
NOTE: `keyup` does not fire on webView input autocomplete.
      so we have to use watch to detect input.
*/
watch(() => email.value, handleEmailChanged);
const submitEmailLogin = async () => {
  message.value = {};
  errors.value = [];
  try {
    const response = await sendLoginEmail(email.value);
    emit("emailSent", response.email);
  } catch (err: unknown) {
    const error = err as AxiosError;
    errors.value = [error];
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
    await loadUser(); // make sure user data is fully loaded
    if (props.next) {
      const url = new URL(props.next, window.location.origin);
      await router.push({
        path: url.pathname,
        hash: url.hash,
      });
      // NOTE: do we really need to reload the page?
      // document.location.reload();
    } else {
      // NOTE: do we really need to reload the page?
      // document.location.reload();
    }
  } catch (err: unknown) {
    const error = err as AxiosError;
    errors.value = [error];
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

// auto-submit form in case of an existing account
whenever(emailExists, async () => {
  if (!promptPassword.value) {
    await submitForm();
  }
});
</script>

<template>
  <pre v-text="{ next }" />
  <form class="form" @submit.prevent="submitForm">
    <div class="input-container">
      <i18n-t keypath="account.auth.usingEmail" tag="label" for="email-1625" />
      <input
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
      <ApiErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton class="button" @click.prevent="submitForm" :disabled="!emailValid">
        {{ buttonText }}
      </AsyncButton>
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

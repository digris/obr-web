<script lang="ts">
import debounce from 'lodash.debounce';
import * as EmailValidator from 'email-validator';
import { defineComponent, ref, computed } from 'vue';
import { useStore } from 'vuex';

import { checkLoginEmail, sendLoginEmail } from '@/api/account';
import APIErrors from '@/components/ui/error/APIErrors.vue';
import Message from '@/components/ui/Message.vue';
import TokenInput from '@/components/account/TokenInput.vue';

const CREATE_ACCOUNT = 'Konto erstellen';
const SEND_TOKEN = 'Code senden';
const LOGIN = 'Login';

export enum Flow {
  Password = 'password',
  Token = 'token',
  Register = 'register',
}

export default defineComponent({
  components: {
    APIErrors,
    Message,
    TokenInput,
  },
  setup() {
    const store = useStore();
    const email = ref('');
    const password = ref('');
    const token = ref('');
    const emailExists = ref(false);
    const emailSent = ref(false);
    const promptPassword = ref(false);
    const buttonText = ref(CREATE_ACCOUNT);
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
    const promptToken = computed(() => {
      if (flow.value === Flow.Password) {
        return false;
      }
      return emailSent.value;
    });
    const updateAccount = (account: any | null) => {
      message.value = '';
      if (account && account.uid) {
        emailExists.value = true;
        if (account.hasUsablePassword) {
          promptPassword.value = true;
          buttonText.value = LOGIN;
        } else {
          message.value = {
            level: 'info',
            body: 'Konto bereits vorhanden. Klicke auf ***',
          };
          buttonText.value = SEND_TOKEN;
        }
      } else {
        emailExists.value = false;
        promptPassword.value = false;
        buttonText.value = CREATE_ACCOUNT;
      }
    };
    const handleEmailInput = debounce(async (e: any) => {
      const { value } = e.target;
      emailExists.value = false;
      promptPassword.value = false;
      if (EmailValidator.validate(value)) {
        const account = await checkLoginEmail(value);
        updateAccount(account);
      }
    }, 200);
    const submitForm = async () => {
      message.value = {};
      errors.value = [];
      console.debug(email.value, promptToken.value);
      if (email.value && promptToken.value) {
        console.debug('submit - token login');
        const credentials = {
          email: email.value,
          token: token.value,
        };
        errors.value = [];
        try {
          await store.dispatch('account/loginUserByToken', credentials);
          document.location.reload();
        } catch (err) {
          console.warn(err);
          errors.value = [err.response];
        }
        return;
      }
      if (flow.value === Flow.Password) {
        console.debug('submit - password');
        const credentials = {
          email: email.value,
          password: password.value,
        };
        errors.value = [];
        try {
          await store.dispatch('account/loginUser', credentials);
          document.location.reload();
        } catch (err) {
          console.warn(err);
          errors.value = [err.response];
        }
        return;
      }
      if (flow.value === Flow.Token) {
        console.debug('submit - token');
        emailSent.value = false;
        try {
          const response = await sendLoginEmail(email.value);
          console.debug(response);
          emailSent.value = true;
          buttonText.value = LOGIN;
          message.value = {
            level: 'info',
            body: response.message,
          };
        } catch (err: any) {
          console.warn(err);
          emailSent.value = false;
          errors.value = [err.response];
        }
        return;
      }
      if (flow.value === Flow.Register) {
        console.debug('submit - register');
        emailSent.value = false;
        try {
          const response = await sendLoginEmail(email.value);
          console.debug(response);
          emailSent.value = true;
          buttonText.value = LOGIN;
          message.value = {
            level: 'info',
            body: response.message,
          };
        } catch (err: any) {
          console.warn(err);
          emailSent.value = false;
          errors.value = [err.response];
        }
      }
    };
    return {
      flow,
      email,
      password,
      token,
      emailExists,
      promptPassword,
      promptToken,
      buttonText,
      message,
      errors,
      handleEmailInput,
      submitForm,
    };
  },
});
</script>

<template>
  <div
    class="form-errors"
    v-if="errors.length"
  >
    <APIErrors
      :errors="errors"
    />
  </div>
  <div
    class="form-messages"
    v-if="(message && message.body)"
  >
    <Message
      :level="message.level"
      :body="message.body"
    />
  </div>
  <form
    class="form"
    @submit.prevent="submitForm"
  >
    <div
      class="input-container"
    >
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
      >
      <label
        for="email-1625"
      >
        E-Mail
      </label>
    </div>
    <div
      v-if="(flow === 'password')"
      class="input-container"
    >
      <input
        class="input"
        v-model="password"
        required
        id="password-1625"
        name="password"
        type="password"
        placeholder="Password"
        autocomplete="current-password"
      >
      <label
        for="password-1625"
      >
        Password
      </label>
    </div>
    <div
      v-if="promptToken"
      class="input-container token-input"
    >
      <p>
        Code aus E-Mail...
      </p>
      <TokenInput
        :token="token"
        @input="token = $event"
      />
      <!--
      <input
        class="input"
        v-model="token"
        required
        id="token-1625"
        name="token"
        type="text"
        placeholder="Code"
      >
      <label
        for="token-1625"
      >
        Code
      </label>
      -->
    </div>
    <div
      class="input-container"
    >
      <button
        class="button"
        type="submit"
        v-text="buttonText"
      />
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";
.form {
  @include form.default;
  display: flex;
  flex-direction: column;
  .input-container {
    @include form.float-label;
    width: 100%;
  }
  .token-input {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
  }
}
.form-messages,
.form-errors {
  margin: 1rem 0;
}
</style>

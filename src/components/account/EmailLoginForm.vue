<script lang="ts">
// import debounce from 'lodash.debounce';
import { debounce } from 'lodash-es';
import * as EmailValidator from 'email-validator';
import { defineComponent, ref, computed } from 'vue';
import { useStore } from 'vuex';

import { checkLoginEmail, sendLoginEmail } from '@/api/account';
import AsyncButton from '@/components/ui/button/AsyncButton.vue';
import APIErrors from '@/components/ui/error/APIErrors.vue';
import Message from '@/components/ui/Message.vue';

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
    AsyncButton,
    APIErrors,
    Message,
  },
  emits: [
    'emailSent',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const email = ref('');
    const password = ref('');
    const emailValid = ref(false);
    const emailExists = ref(false);
    const promptPassword = ref(false);
    const buttonText = ref(LOGIN);
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
      message.value = '';
      if (account && account.uid) {
        emailExists.value = true;
        if (account.hasUsablePassword) {
          promptPassword.value = true;
          buttonText.value = LOGIN;
        } else {
          message.value = {
            level: 'info',
            body: 'Konto bereits vorhanden. Klicke auf "Code senden"',
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
        buttonText.value = LOGIN;
      }
    }, 200);
    const submitForm = async () => {
      message.value = {};
      errors.value = [];
      if (flow.value === Flow.Register || flow.value === Flow.Token) {
        try {
          const response = await sendLoginEmail(email.value);
          emit('emailSent', response.email);
        } catch (err: any) {
          console.warn(err);
          errors.value = [err.response];
        }
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
      }
    };
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
    };
  },
});
</script>

<template>
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
      class="form-messages"
      v-if="(message && message.body)"
    >
      <Message
        :level="message.level"
        :body="message.body"
      />
    </div>
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
        :disabled="(!emailValid)"
      >
        {{ buttonText }}
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
}
.form-messages,
.form-errors {
  margin: 1rem 0;
}
</style>

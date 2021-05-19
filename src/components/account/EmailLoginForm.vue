<script lang="ts">
import debounce from 'lodash.debounce';
import * as EmailValidator from 'email-validator';
import { defineComponent, ref } from 'vue';

import { checkLoginEmail, sendLoginEmail } from '@/api/account';

export default defineComponent({
  setup() {
    const email = ref('');
    const emailAlreadyRegistered = ref(false);
    const token = ref('');
    const errors = ref<Array<String>>([]);
    const message = ref('');
    const handleEmailInput = debounce(async (e: any) => {
      const { value } = e.target;
      emailAlreadyRegistered.value = false;
      if (EmailValidator.validate(value)) {
        const account = await checkLoginEmail(value);
        emailAlreadyRegistered.value = !!(account && account.uid);
      }
    }, 200);
    const submitForm = async () => {
      errors.value = [];
      try {
        const response = await sendLoginEmail(email.value);
        message.value = response.message;
      } catch (err: any) {
        console.warn(err);
        errors.value = [err.message, err.response.data];
      }
    };
    return {
      email,
      emailAlreadyRegistered,
      token,
      errors,
      message,
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
    <pre v-text="errors" />
  </div>
  <div
    v-if="message"
  >
    <p>{{ message }}</p>
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
        autocomplete="username"
      >
      <label
        for="email-1625"
      >
        E-Mail
      </label>
    </div>
    <!--
    <label
      class="input-container"
    >
      <input
        class="input"
        v-model="token"
        name="token"
        type="text"
        placeholder="Token"
      >
    </label>
    -->
    <div
      v-if="emailAlreadyRegistered"
      class="input-container"
    >
      <p
      >
        Für <em>{{ email }}</em> ist bereits ein Konto vorhanden.<br>
        Klicke auf "Login link senden".
      </p>
    </div>
    <div
      class="input-container"
    >
      <button
        v-if="emailAlreadyRegistered"
        class="button"
        type="submit"
      >
        Login link senden
      </button>
      <button
        v-else
        class="button"
        type="submit"
      >
        Konto erstellen
      </button>
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
}
</style>

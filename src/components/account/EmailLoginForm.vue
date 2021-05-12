<script lang="ts">
import debounce from 'lodash.debounce';
import * as EmailValidator from 'email-validator';
import { defineComponent, ref } from 'vue';

import { sendLoginEmail } from '@/api/account';

export default defineComponent({
  setup() {
    const email = ref('');
    const token = ref('');
    const errors = ref<Array<String>>([]);
    const message = ref('');
    const handleEmailInput = debounce((e: any) => {
      const { value } = e.target;
      const isValid = EmailValidator.validate(value);
      console.debug('value', value, 'valid', isValid);
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
    <label
      class="input-container"
    >
      <input
        class="input"
        @input="handleEmailInput"
        v-model="email"
        required
        name="email"
        type="email"
        placeholder="E-Mail"
        autocomplete="on"
      >
    </label>
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
      class="input-container"
    >
      <button
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
    width: 100%;
  }
}
</style>

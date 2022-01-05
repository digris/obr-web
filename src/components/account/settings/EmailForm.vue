<script lang="ts">
import {
  defineComponent,
  ref,
} from 'vue';

import * as EmailValidator from 'email-validator';

import { updateEmail } from '@/api/account';

import AsyncButton from '@/components/ui/button/AsyncButton.vue';
import APIErrors from '@/components/ui/error/APIErrors.vue';
import TextInput from '@/components/ui/form/TextInput.vue';

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    TextInput,
  },
  props: {
    currentEmail: {
      type: String,
      required: true,
      default: '',
    },
  },
  emits: [
    'updated',
  ],
  setup(props, { emit }) {
    const email = ref(props.currentEmail);
    const formValid = ref(false);
    const errors = ref<Array<string>>([]);
    const handleInput = () => {
      formValid.value = EmailValidator.validate(email.value);
    };
    const submitForm = async () => {
      errors.value = [];
      try {
        await updateEmail(email.value);
        emit('updated');
      } catch (err: any) {
        console.warn(err);
        errors.value = [err.response];
      }
    };
    return {
      email,
      errors,
      handleInput,
      formValid,
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
      <TextInput
        v-model="email"
        @keyup="handleInput"
        type="email"
        label="E-Mail Adresse"
        :minlength="(8)"
        :maxlength="(64)"
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
        :disabled="(!formValid)"
      >
        Speichern
      </AsyncButton>
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";
.form {
  @include form.default;
  .input-container {
    @include form.top-label;
  }
}
</style>

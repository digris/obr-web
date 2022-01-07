<script lang="ts">
import {
  defineComponent,
  ref,
} from 'vue';

import { updateUser } from '@/api/account';

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
    user: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  emits: [
    'updated',
  ],
  setup(props, { emit }) {
    const firstName = ref(props.user.firstName);
    const lastName = ref(props.user.lastName);
    const formValid = ref(false);
    const errors = ref<Array<string>>([]);
    const submitForm = async () => {
      errors.value = [];
      try {
        await updateUser({
          firstName: firstName.value,
          lastName: lastName.value,
        });
        emit('updated');
      } catch (err: any) {
        console.warn(err);
        errors.value = [err.response];
      }
    };
    return {
      firstName,
      lastName,
      formValid,
      errors,
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
        v-model="firstName"
        type="text"
        label="Name"
      />
    </div>
    <div
      class="input-container"
    >
      <TextInput
        v-model="lastName"
        type="text"
        label="Nachname"
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

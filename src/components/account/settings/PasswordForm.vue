<script lang="ts">
import { defineComponent, ref } from "vue";

import { updatePassword } from "@/api/account";

import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import TextInput from "@/components/ui/form/TextInput.vue";

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    TextInput,
  },
  emits: ["updated"],
  setup(props, { emit }) {
    const password = ref("");
    const passwordConfirm = ref("");
    const formValid = ref(false);
    const errors = ref<Array<string>>([]);
    const handleInput = () => {
      formValid.value = password.value.length > 0 && password.value === passwordConfirm.value;
    };
    const submitForm = async () => {
      errors.value = [];
      try {
        await updatePassword(password.value);
        emit("updated");
      } catch (err: any) {
        console.warn(err);
        errors.value = [err.response];
      }
    };
    return {
      password,
      passwordConfirm,
      errors,
      handleInput,
      formValid,
      submitForm,
    };
  },
});
</script>

<template>
  <form class="form" @submit.prevent="submitForm">
    <div class="input-container">
      <TextInput
        v-model="password"
        @keyup="handleInput"
        type="password"
        label="Neues Passwort"
        autocomplete="new-password"
        placeholder="Passwort"
        :minlength="8"
        :maxlength="64"
      />
    </div>
    <div class="input-container">
      <TextInput
        v-model="passwordConfirm"
        @keyup="handleInput"
        type="password"
        label="Passwort bestätigen"
        autocomplete="new-password"
        placeholder="Passwort"
        :minlength="8"
        :maxlength="64"
      />
    </div>
    <div class="form-errors" v-if="errors.length">
      <APIErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton class="button" @click.prevent="submitForm" :disabled="!formValid">
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

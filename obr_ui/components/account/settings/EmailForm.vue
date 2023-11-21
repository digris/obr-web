<script lang="ts" setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import * as EmailValidator from "email-validator";
import type { AxiosError } from "axios";

import { updateEmail } from "@/api/account";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import TextInput from "@/components/ui/form/TextInput.vue";

const props = defineProps<{
  currentEmail: string;
}>();

const emit = defineEmits(["updated"]);

const { t } = useI18n();
const email = ref(props.currentEmail);
const formValid = ref(false);
const errors = ref<Array<string | AxiosError>>([]);
const handleInput = () => {
  formValid.value = EmailValidator.validate(email.value);
};
const submitForm = async () => {
  errors.value = [];
  try {
    await updateEmail(email.value);
    emit("updated");
  } catch (err: unknown) {
    const error = err as AxiosError;
    errors.value = [error];
  }
};
</script>

<template>
  <form class="form" @submit.prevent="submitForm">
    <div class="input-container">
      <TextInput
        v-model="email"
        @keyup="handleInput"
        type="email"
        :label="t('account.settings.email.labelEmail')"
        :minlength="8"
        :maxlength="64"
      />
    </div>
    <div class="form-errors" v-if="errors.length">
      <ApiErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton
        class="button"
        @click.prevent="submitForm"
        :disabled="!formValid"
        v-text="t('formActions.save')"
      />
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

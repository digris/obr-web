<script lang="ts">
import { defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";

import { updatePassword } from "@/api/account";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import TextInput from "@/components/ui/form/TextInput.vue";
import { useAccount } from "@/composables/account";

export default defineComponent({
  components: {
    AsyncButton,
    ApiErrors,
    TextInput,
  },
  emits: ["updated"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { user } = useAccount();
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
      t,
      user,
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
    <!--
    we include a hidden reference for the "username" to coop with password managers
    https://www.chromium.org/developers/design-documents/create-amazing-password-forms/
    -->
    <input v-show="false" type="email" autocomplete="username" :value="user.email" />
    <div class="input-container">
      <TextInput
        v-model="password"
        @keyup="handleInput"
        type="password"
        autocomplete="new-password"
        :label="t('account.settings.password.labelPassword')"
        :placeholder="t('account.settings.password.placeholderPassword')"
        :minlength="8"
        :maxlength="64"
      />
    </div>
    <div class="input-container">
      <TextInput
        v-model="passwordConfirm"
        @keyup="handleInput"
        type="password"
        autocomplete="new-password"
        :label="t('account.settings.password.labelPasswordConfirm')"
        :placeholder="t('account.settings.password.placeholderPasswordConfirm')"
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

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";

import { updateUser } from "@/api/account";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import SelectInput from "@/components/ui/form/SelectInput.vue";
import TextInput from "@/components/ui/form/TextInput.vue";

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    TextInput,
    SelectInput,
  },
  props: {
    user: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  emits: ["updated"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const gender = ref(props.user.gender);
    const genderOptions = [
      {
        value: "female",
        name: t("account.settings.personal.gender.options.female"),
      },
      {
        value: "male",
        name: t("account.settings.personal.gender.options.male"),
      },
      {
        value: "other",
        name: t("account.settings.personal.gender.options.other"),
      },
    ];
    const firstName = ref(props.user.firstName);
    const lastName = ref(props.user.lastName);
    const favoriteVenue = ref(props.user.favoriteVenue);
    const yearOfBirth = ref(props.user.yearOfBirth);
    const formValid = ref(false);
    const errors = ref<Array<string>>([]);
    const formErrors = ref<Array<string>>([]);
    const submitForm = async () => {
      errors.value = [];
      formErrors.value = [];
      try {
        await updateUser({
          gender: gender.value,
          firstName: firstName.value,
          lastName: lastName.value,
          favoriteVenue: favoriteVenue.value,
          yearOfBirth: yearOfBirth.value ? yearOfBirth.value : null,
        });
        emit("updated");
      } catch (err: any) {
        console.error(err.response.data);
        errors.value = [err.response];
        formErrors.value = err.response.data;
      }
    };
    return {
      t,
      gender,
      genderOptions,
      firstName,
      lastName,
      yearOfBirth,
      favoriteVenue,
      formValid,
      errors,
      formErrors,
      submitForm,
    };
  },
});
</script>

<template>
  <form class="form" @submit.prevent="submitForm">
    <div class="input-container">
      <TextInput
        v-model="firstName"
        type="text"
        :label="t('account.settings.personal.labelName')"
      />
    </div>
    <div class="input-container">
      <TextInput
        v-model="lastName"
        type="text"
        :label="t('account.settings.personal.labelSurname')"
      />
    </div>
    <div class="input-container input-container--2-2">
      <TextInput
        v-model="yearOfBirth"
        type="number"
        :min-value="1900"
        :max-value="2022"
        placeholder="19?? / 20??"
        :label="t('account.settings.personal.labelYearOfBirth')"
        :errors="formErrors?.yearOfBirth ?? []"
      />
      <SelectInput
        v-model="gender"
        :options="genderOptions"
        type="text"
        :label="t('account.settings.personal.gender.label')"
      />
    </div>
    <div class="input-container">
      <TextInput
        v-model="favoriteVenue"
        type="text"
        :label="t('account.settings.personal.labelFavoriteVenue')"
      />
    </div>
    <div class="form-errors" v-if="errors.length">
      <APIErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton class="button" @click.prevent="submitForm" v-text="t('formActions.save')" />
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";

.form {
  @include form.default;

  .input-container {
    @include form.top-label;

    :deep(input) {
      &::placeholder {
        color: rgb(var(--c-dark) / 20%);
      }
    }

    &--2-2 {
      display: grid;
      grid-gap: 1rem;
      grid-template-columns: 2fr 2fr;
    }
  }
}
</style>

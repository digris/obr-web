<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import type { AxiosError } from "axios";

import { getAddressCountries, updateAddress } from "@/api/account";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import ApiErrors from "@/components/ui/error/ApiErrors.vue";
import SelectInput from "@/components/ui/form/SelectInput.vue";
import TextInput from "@/components/ui/form/TextInput.vue";
import type { Address } from "@/typings";

const props = defineProps<{
  address: Address;
}>();

const emit = defineEmits(["updated"]);

const { t } = useI18n();
const countryOptions = ref<Array<{ value: string; name: string }>>([]);
const line1 = ref(props.address.line1);
const line2 = ref(props.address.line2);
const postalCode = ref(props.address.postalCode);
const city = ref(props.address.city);
const country = ref(props.address.country);
const errors = ref<Array<string | AxiosError>>([]);
const submitForm = async () => {
  errors.value = [];
  try {
    await updateAddress({
      line1: line1.value,
      line2: line2.value,
      postalCode: postalCode.value,
      city: city.value,
      country: country.value,
    });
    emit("updated");
  } catch (err: unknown) {
    const error = err as AxiosError;
    errors.value = [error];
  }
};
onMounted(async () => {
  if (!countryOptions.value.length) {
    const countries = await getAddressCountries();
    countryOptions.value = countries.map((item) => {
      return { value: item.iso2Code, name: item.name };
    });
  }
});
</script>

<template>
  <form class="form" @submit.prevent="submitForm">
    <div class="input-container">
      <TextInput v-model="line1" type="text" :label="t('account.settings.address.labelLine1')" />
    </div>
    <div class="input-container">
      <TextInput v-model="line2" type="text" :label="t('account.settings.address.labelLine2')" />
    </div>
    <div class="input-container input-container--1-3">
      <TextInput
        v-model="postalCode"
        type="text"
        :label="t('account.settings.address.labelPostalCode')"
      />
      <TextInput v-model="city" type="text" :label="t('account.settings.address.labelCity')" />
    </div>
    <div class="input-container">
      <SelectInput
        v-model="country"
        :options="countryOptions"
        type="text"
        :label="t('account.settings.address.labelCountry')"
      />
    </div>
    <div class="form-errors" v-if="errors.length">
      <ApiErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton class="button" @click.prevent="submitForm">
        {{ t("formActions.save") }}
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

    &--1-3 {
      display: grid;
      grid-gap: 1rem;
      grid-template-columns: 1fr 3fr;
    }
  }
}
</style>

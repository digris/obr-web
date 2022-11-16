<script lang="ts">
import type { PropType } from "vue";
import { defineComponent, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import type { Address } from "@/typings/api";
import { getAddressCountries, updateAddress } from "@/api/account";

import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import TextInput from "@/components/ui/form/TextInput.vue";
import SelectInput from "@/components/ui/form/SelectInput.vue";

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    TextInput,
    SelectInput,
  },
  props: {
    address: {
      type: Object as PropType<Address>,
      required: true,
      default: () => ({}),
    },
  },
  emits: ["updated"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const countryOptions = ref([]);
    const line1 = ref(props.address.line1);
    const line2 = ref(props.address.line2);
    const postalCode = ref(props.address.postalCode);
    const city = ref(props.address.city);
    const country = ref(props.address.country);
    const formValid = ref(false);
    const errors = ref<Array<string>>([]);
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
      } catch (err: any) {
        console.warn(err);
        errors.value = [err.response];
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
    return {
      t,
      line1,
      line2,
      postalCode,
      city,
      country,
      countryOptions,
      formValid,
      errors,
      submitForm,
    };
  },
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
    &--1-3 {
      display: grid;
      grid-gap: 1rem;
      grid-template-columns: 1fr 3fr;
    }
  }
}
</style>

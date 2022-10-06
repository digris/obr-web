<script lang="ts">
import type { PropType } from "vue";
import { defineComponent, onMounted, ref } from "vue";
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
      <TextInput v-model="line1" type="text" label="Adresse" />
    </div>
    <div class="input-container">
      <TextInput v-model="line2" type="text" label="Zusatz" />
    </div>
    <div class="input-container input-container--1-3">
      <TextInput v-model="postalCode" type="text" label="PLZ" />
      <TextInput v-model="city" type="text" label="Ort" />
    </div>
    <div class="input-container">
      <SelectInput v-model="country" :options="countryOptions" type="text" label="Land" />
    </div>
    <div class="form-errors" v-if="errors.length">
      <APIErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton class="button" @click.prevent="submitForm"> Speichern </AsyncButton>
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

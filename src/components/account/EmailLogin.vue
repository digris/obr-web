<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRoute } from "vue-router";
import { useAccount } from "@/composables/account";

export default defineComponent({
  setup() {
    const route = useRoute();
    const { loginUserBySignedEmail } = useAccount();
    const signedEmail = ref(route.params.signedEmail);
    const errors = ref<Array<string>>([]);
    const loginBySignedEmail = async (value: string | string[]) => {
      try {
        await loginUserBySignedEmail(value);
        document.location.href = "/account/settings/";
      } catch (err) {
        console.warn(err);
        errors.value = [err.message, err.response.data];
      }
    };
    if (signedEmail.value) {
      loginBySignedEmail(signedEmail.value);
    }
    return {
      errors,
      signedEmail,
    };
  },
});
</script>
<template>
  <div class="form-errors" v-if="errors.length">
    <pre v-text="errors" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import EmailLoginForm from '@/components/account/EmailLoginForm.vue';

export default defineComponent({
  components: {
    EmailLoginForm,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const signedEmail = ref(route.params.signedEmail);
    // const errors = ref([]);
    const errors = ref<Array<String>>([]);
    const loginBySignedEmail = async (value: string | string[]) => {
      console.debug('loginBySignedEmail', value);
      console.debug('store', store);
      try {
        await store.dispatch('account/loginUserBySignedEmail', value);
        await router.push({ name: 'Account' });
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
  <h1>Email Login</h1>
  <div
    class="form-errors"
    v-if="errors.length"
  >
    <pre v-text="errors" />
  </div>
  <EmailLoginForm />
  <div>
    <p>{{ signedEmail }}</p>
  </div>
</template>

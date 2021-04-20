<script lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  setup() {
    const router = useRouter();
    const store = useStore();
    const email = ref('');
    const password = ref('');
    const errors = ref([]);
    const submitForm = async () => {
      const credentials = {
        email: email.value,
        password: password.value,
      };
      errors.value = [];
      try {
        await store.dispatch('account/loginUser', credentials);
        await router.push({ name: 'home' });
      } catch (err) {
        console.warn(err);
        // errors.value = ['login error'];
      }
    };
    return {
      email,
      password,
      errors,
      submitForm,
    };
  },
};
</script>

<template>
  <div
    class="form-errors"
    v-if="errors.length"
  >
    <pre v-text="errors" />
  </div>
  <form
    class="form"
    @submit.prevent="submitForm"
  >
    <label>
      <input
        v-model="email"
        required
        name="email"
        type="email"
        placeholder="email"
        autocomplete="username"
      >
    </label>
    <label>
      <input
        v-model="password"
        required
        name="password"
        type="password"
        placeholder="password"
        autocomplete="current-password"
      >
    </label>
    <button
      type="submit"
    >
      Login
    </button>
  </form>
</template>

<style lang="scss" scoped>
.form {
  display: flex;
}
</style>

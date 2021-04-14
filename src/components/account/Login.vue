<script lang="ts">
import { computed, ref } from 'vue';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    const email = ref('');
    const password = ref('');
    const submitForm = () => {
      const credentials = {
        email: email.value,
        password: password.value,
      };
      store.dispatch('account/loginUser', credentials);
    };
    return {
      currentUser,
      email,
      password,
      submitForm,
    };
  },
};
</script>
<template>
  <h1>Login</h1>
  <pre v-text="currentUser" />
  <div>
    e: {{ email }}<br>
    p: {{ password }}<br>
  </div>
  <form
    @submit.prevent="submitForm"
  >
    <input
      v-model="email"
      name="email"
      type="email"
      placeholder="email"
      autocomplete="username"
    >
    <input
      v-model="password"
      name="password"
      type="password"
      placeholder="password"
      autocomplete="current-password"
    >
    <button type="submit">Login</button>
  </form>
</template>

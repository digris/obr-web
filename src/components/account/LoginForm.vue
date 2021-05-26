<script lang="ts">
import { ref } from 'vue';
// import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  setup() {
    // const router = useRouter();
    const store = useStore();
    const email = ref('');
    const password = ref('');
    const errors = ref<Array<String>>([]);
    const message = ref('');
    const submitForm = async () => {
      const credentials = {
        email: email.value,
        password: password.value,
      };
      errors.value = [];
      try {
        await store.dispatch('account/loginUser', credentials);
        // TODO: refresh user related data (ratings etc) instead of location reload
        window.location.reload();
        // await router.push({ name: 'home' });
        // const msg = {
        //   level: 'success',
        //   body: 'foo the blu',
        //   action: {
        //     label: 'More',
        //     url: '/foo/bar/',
        //   },
        // };
        // store.dispatch('notification/addMessage', msg);
      } catch (err) {
        console.warn(err);
        errors.value = [err.message, err.response.data];
      }
    };
    return {
      email,
      password,
      errors,
      message,
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
  <div
    v-if="message"
  >
    <p>{{ message }}</p>
  </div>
  <form
    class="form"
    @submit.prevent="submitForm"
  >
    <div
      class="input-container"
    >
      <input
        class="input"
        v-model="email"
        required
        id="email"
        name="email"
        type="email"
        placeholder="E-Mail"
        autocomplete="username"
      >
      <label
        for="email"
      >
        E-Mail
      </label>
    </div>
    <div
      class="input-container"
    >
      <input
        class="input"
        v-model="password"
        id="password"
        required
        name="password"
        type="password"
        placeholder="Password"
        autocomplete="current-password"
      >
      <label
        for="password"
      >
        Password
      </label>
    </div>
    <div
      class="input-container"
    >
      <button
        class="button"
        type="submit"
      >
        Login
      </button>
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/elements/form";
.form {
  @include form.default;
  display: flex;
  flex-direction: column;
  .input-container {
    @include form.float-label;
    width: 100%;
  }
}
</style>

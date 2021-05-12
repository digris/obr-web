<script lang="ts">
import SocialLogin from '@/components/account/SocialLogin.vue';
import LoginForm from '@/components/account/LoginForm.vue';

export default {
  components: {
    SocialLogin,
    LoginForm,
  },
};
</script>
<template>
  <h1>Login</h1>
  <section
    class="section"
  >
    <SocialLogin />
  </section>
  <section
    class="section"
  >
    <LoginForm />
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
</style>

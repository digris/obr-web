<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import SocialLogin from '@/components/account/SocialLogin.vue';

export default defineComponent({
  components: {
    SocialLogin,
  },
  setup() {
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    const socialNext = window.location.pathname;
    return {
      currentUser,
      socialNext,
    };
  },
});
</script>

<template>
  <section
    class="section"
  >
    <h3
      class="header"
    >User Details</h3>
    <pre
      v-text="currentUser"
      class="_debug"
    />
    <div
      class="info-grid"
    >
      <div
        class="label"
      >Account ID:</div>
      <div
        class="value"
      >{{ currentUser.uid }}</div>
      <div
        class="label"
      >E-Mail:</div>
      <div
        class="value"
      >{{ currentUser.email }}</div>
      <div
        class="label"
      >Name:</div>
      <div
        class="value"
      >
        <span
          v-if="currentUser.firstName"
        >{{ currentUser.firstName }}</span>
        <span
          v-if="currentUser.lastName"
        >{{ currentUser.lastName }}</span>
      </div>
    </div>
  </section>
  <section
    class="section"
  >
    <h3
      class="header"
    >Change Password</h3>
    <div>
      ...
    </div>
  </section>
  <section
    class="section"
  >
    <h3
      class="header"
    >Connect Accounts</h3>
    <div>
      <SocialLogin
        :next="socialNext"
      />
    </div>
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
.info-grid {
  display: grid;
  grid-gap: 0.5rem;
  grid-template-columns: auto 1fr;
  .label {
    opacity: 0.5;
  }
}
</style>

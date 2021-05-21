<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import SocialLogin from '@/components/account/SocialLogin.vue';
import SettingsSubscription from '@/components/account/settings/SettingsSubscription.vue';

export default defineComponent({
  components: {
    SocialLogin,
    SettingsSubscription,
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
    v-if="currentUser"
    class="section"
  >
    <h3
      class="header"
    >Plan / Subscription</h3>
    <SettingsSubscription
      :user="currentUser"
    />
  </section>
  <section
    v-if="currentUser"
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
      >ID:</div>
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
@use "@/style/elements/info-grid";
.section {
  @include section.default;
}
.info-grid {
  @include info-grid.default;
}
</style>

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
    <div>
      <pre
        v-text="currentUser"
        class="debug"
      />
    </div>
  </section>
  <section
    class="section"
  >
    <h3
      class="header"
    >Change Password</h3>
    <div>
      (( Bar ))
    </div>
  </section>
  <section
    class="section"
  >
    <h3
      class="header"
    >Link Accounts</h3>
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
</style>

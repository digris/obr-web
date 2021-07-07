<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import SocialLogin from '@/components/account/SocialLogin.vue';
import Subscription from '@/components/account/settings/SettingsSubscription.vue';
import Section from '@/components/account/settings/SettingsSection.vue';

export default defineComponent({
  components: {
    Section,
    SocialLogin,
    Subscription,
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
  <Section
    v-if="currentUser"
    title="Guthaben für kostenpflichtige Inhalte"
  >
    <Subscription
      :user="currentUser"
    />
  </Section>
  <Section
    v-if="currentUser"
    title="Persönliche Angaben"
  >
    <div
      class="user-details"
    >
      <p
        v-text="currentUser.email"
      />
      <p>
        <span
          v-if="currentUser.firstName"
          v-text="currentUser.firstName"
        />
        <span
          v-if="currentUser.lastName"
          v-text="currentUser.lastName"
        />
      </p>
      <p
        v-text="`ID: ${currentUser.uid}`"
      />
    </div>
  </Section>
  <Section
    v-if="currentUser"
    title="Verbundene Accounts"
    :outlined="(false)"
  >
    <SocialLogin
      :next="socialNext"
    />
  </Section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.section {
  margin: 2rem 0;
  :deep(.title) {
    padding-bottom: 0.4rem;
  }
  :deep(.panel) {
    padding-top: 0.75rem;
  }
  &.is-outlined {
    :deep(.panel) {
      padding: 0.75rem;
      border: 1px solid rgb(var(--c-gray-200));
    }
  }
}
.user-details {
  @include typo.large;
}
</style>

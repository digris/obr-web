<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import SocialLogin from '@/components/account/SocialLogin.vue';
import Section from '@/components/account/settings/SettingsSection.vue';
import CurrentSubscription from '@/components/subscription/CurrentSubscription.vue';
import Debug from '@/components/dev/Debug.vue';

export default defineComponent({
  components: {
    Section,
    SocialLogin,
    CurrentSubscription,
    Debug,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters['account/user']);
    const subscription = computed(() => store.getters['account/subscription']);
    const settings = computed(() => store.getters['account/settings']);
    const socialNext = window.location.pathname;
    return {
      user,
      subscription,
      settings,
      socialNext,
    };
  },
});
</script>

<template>
  <Section
    v-if="user"
    title="Guthaben für kostenpflichtige Inhalte"
  >
    <CurrentSubscription />
  </Section>
  <Section
    v-if="user"
    title="Persönliche Angaben"
  >
    <div
      class="user-details"
    >
      <p
        v-text="user.email"
      />
      <p>
        <span
          v-if="user.firstName"
          v-text="user.firstName"
        />
        <span
          v-if="user.lastName"
          v-text="user.lastName"
        />
      </p>
      <p
        v-text="`ID: ${user.uid}`"
      />
    </div>
  </Section>
  <Section
    v-if="user"
    title="Verbundene Accounts"
    :outlined="(false)"
  >
    <SocialLogin
      :next="socialNext"
    />
  </Section>
  <Section
    title="Debug"
    :outlined="(false)"
  >
    <Debug
      title="user"
      :value="user"
    />
    <Debug
      title="subscription"
      :value="subscription"
    />
    <Debug
      title="settings"
      :value="settings"
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

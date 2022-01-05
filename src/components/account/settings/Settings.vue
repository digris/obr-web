<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import SocialLogin from '@/components/account/SocialLogin.vue';
import Section from '@/components/account/settings/Section.vue';
import CurrentSubscription from '@/components/subscription/CurrentSubscription.vue';
import Password from '@/components/account/settings/Password.vue';
import Debug from '@/components/dev/Debug.vue';

export default defineComponent({
  components: {
    Section,
    SocialLogin,
    CurrentSubscription,
    Password,
    Debug,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters['account/user']);
    const subscription = computed(() => store.getters['account/subscription']);
    const settings = computed(() => store.getters['account/settings']);
    const address = computed(() => store.getters['account/address']);
    const fullName = computed(() => {
      if (user.value?.firstName && user.value?.lastName) {
        return `${user.value.firstName} ${user.value.lastName}`;
      }
      if (user.value?.firstName) {
        return user.value.firstName;
      }
      if (user.value?.lastName) {
        return user.value.lastName;
      }
      return null;
    });
    const socialNext = window.location.pathname;
    return {
      user,
      subscription,
      settings,
      address,
      fullName,
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
    title="E-Mail"
  >
    <p
      class="user-details"
      v-text="user.email"
    />
  </Section>
  <Password />
  <Section
    v-if="user"
    title="Name"
  >
    <div
      class="user-details"
    >
      <p
        v-if="fullName"
        v-text="fullName"
      />
      <p
        v-else
        v-text="`---`"
      />
    </div>
  </Section>
  <Section
    v-if="user"
    title="Adresse"
  >
    <div
      class="user-details"
    >
      <div
        v-if="address"
      >
        <p
          v-if="address.line1"
          v-text="address.line1"
        />
        <p
          v-if="address.line2"
          v-text="address.line2"
        />
        <p>
          <span
            v-if="address.country"
            v-text="`${address.country}${address.postalCode ? '-' : ''}`"
          />
          <span
            v-if="address.postalCode"
            v-text="`${address.postalCode}${address.country ? ' ' : ''}`"
          />
          <span
            v-if="address.city"
            v-text="address.city"
          />
        </p>
      </div>
      <p
        v-else
        v-text="`---`"
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
    v-if="(false)"
    title="Debug"
    :outlined="(false)"
  >
    <Debug
      title="user"
      :value="user"
    />
    <Debug
      title="address"
      :value="address"
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
}
.user-details {
  @include typo.large;
}
</style>

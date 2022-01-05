<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import SocialLogin from '@/components/account/SocialLogin.vue';
import Section from '@/components/account/settings/Section.vue';
import CurrentSubscription from '@/components/subscription/CurrentSubscription.vue';
import Password from '@/components/account/settings/Password.vue';
import Email from '@/components/account/settings/Email.vue';
import Address from '@/components/account/settings/Address.vue';
// import Debug from '@/components/dev/Debug.vue';

export default defineComponent({
  components: {
    Section,
    SocialLogin,
    CurrentSubscription,
    Email,
    Password,
    Address,
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
  <Email
    v-if="user"
    :user="user"
  />
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
  <Address
    :address="address"
  />
  <Section
    v-if="user"
    title="Verbundene Accounts"
    :outlined="(false)"
  >
    <SocialLogin
      :next="socialNext"
    />
  </Section>
</template>

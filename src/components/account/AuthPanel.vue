<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';
import SidePanel from '@/components/ui/panel/SidePanel.vue';

import SocialLogin from '@/components/account/SocialLogin.vue';
import EmailLoginForm from '@/components/account/EmailLoginForm.vue';
import EmailLoginVerify from '@/components/account/EmailLoginVerify.vue';

export default defineComponent({
  components: {
    SidePanel,
    SocialLogin,
    EmailLoginForm,
    EmailLoginVerify,
  },
  setup() {
    const store = useStore();
    const isVisible = ref(false);
    const socialLoginVisible = ref(true);
    const emailLoginVisible = ref(true);
    const emailLoginVerifyVisible = ref(false);
    const intent = ref('login');
    const next = ref(null);
    const message = ref(null);
    const emailSent = ref(false);
    const close = () => {
      isVisible.value = false;
    };
    const setIntent = (value: string) => {
      intent.value = value;
    };
    const handleEmailSent = () => {
      emailSent.value = true;
      socialLoginVisible.value = false;
      emailLoginVisible.value = false;
      emailLoginVerifyVisible.value = true;
    };
    eventBus.on('account:authenticate', (event) => {
      isVisible.value = true;
      if (event.intent) {
        intent.value = event.intent;
      }
      next.value = event.next || null;
      message.value = event.message || null;
    });
    store.watch((state: any) => state.account.currentUser, (newUser) => {
      if (newUser) {
        isVisible.value = false;
      }
    });
    return {
      close,
      isVisible,
      socialLoginVisible,
      emailLoginVisible,
      emailLoginVerifyVisible,
      next,
      intent,
      setIntent,
      message,
      handleEmailSent,
    };
  },
});
</script>
<template>
  <SidePanel
    :is-visible="isVisible"
    @close="close"
  >
    <div
      class="title"
    >
      Anmelden
    </div>
    <div
      v-if="message"
      class="message"
    >
      <p>{{ message }}</p>
    </div>
    <section
      v-if="socialLoginVisible"
      class="section social"
    >
      <p>Mit einem bestehenden Konto:</p>
      <SocialLogin
        :next="next"
      />
    </section>
    <div
      v-if="(socialLoginVisible && emailLoginVisible)"
      class="subtitle"
    >
      oder
    </div>
    <section
      v-if="emailLoginVisible"
      class="section email"
    >
      <p>Mit deiner E-Mail-Adresse:</p>
      <EmailLoginForm
        @email-sent="handleEmailSent"
      />
    </section>
    <section
      v-if="emailLoginVerifyVisible"
      class="section email"
    >
      <EmailLoginVerify />
    </section>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/section";
.section {
  @include section.default;
}
.title {
  @include typo.x-large;
  @include typo.bold;
  display: flex;
  justify-content: flex-start;
}
.subtitle {
  @include typo.large;
  display: flex;
  justify-content: flex-start;
}
.social {
  > p {
    margin-bottom: 1rem;
  }
}
.email {
  > p {
    margin-bottom: 0.5rem;
  }
}
.lead {
  @include typo.large;
  a {
    text-decoration: underline;
    cursor: pointer;
  }
}
.message {
  margin: 1rem 0 1rem;
  padding: 1rem;
  background: rgba(var(--c-cta), 0.1);
  border-left: 4px solid rgb(var(--c-cta));
}
</style>

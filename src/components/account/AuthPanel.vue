<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';
import SidePanel from '@/components/ui/SidePanel.vue';
// import SidePanel from '@/components/ui/Modal.vue';
import SocialLogin from '@/components/account/SocialLogin.vue';
import LoginForm from '@/components/account/LoginForm.vue';
import EmailLoginForm from '@/components/account/EmailLoginForm.vue';

export default defineComponent({
  components: {
    SidePanel,
    SocialLogin,
    LoginForm,
    EmailLoginForm,
  },
  setup() {
    const store = useStore();
    const isVisible = ref(false);
    const intent = ref('login');
    const next = ref(null);
    const message = ref(null);
    const close = () => {
      isVisible.value = false;
    };
    const setIntent = (value: string) => {
      intent.value = value;
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
      intent,
      next,
      setIntent,
      message,
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
      class="intents"
    >
      <h1
        @click="setIntent('register')"
        class="intent"
        :class="{'is-selected': (intent === 'register')}"
      >
        Sign-Up
      </h1>
      <h1
        @click="setIntent('login')"
        class="intent"
        :class="{'is-selected': (intent === 'login')}"
      >
        Login
      </h1>
    </div>
    <div
      v-if="message"
      class="message"
    >
      <p>{{ message }}</p>
    </div>
    <section
      class="section social"
    >
      <SocialLogin
        :next="next"
      />
    </section>
    <section
      class="section email"
    >
      <p>Oder anmelden mit:</p>
      <EmailLoginForm />
    </section>
    <section
      v-if="(intent === 'login')"
      class="section email"
    >
      <LoginForm />
    </section>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
.intents {
  display: flex;
  justify-content: center;
  .intent {
    //padding: 0 1rem;
    cursor: pointer;
    &:not(:first-child) {
      margin-left: 2rem;
    }
    &.is-selected {
      text-decoration: underline;
    }
  }
}
.message {
  margin: 2rem 0 2rem;
  padding: 1rem;
  //color: rgb(var(--c-white));
  //background: rgb(var(--c-black));
  background: rgba(var(--c-cta), 0.1);
  border-left: 4px solid rgb(var(--c-cta));
}
</style>

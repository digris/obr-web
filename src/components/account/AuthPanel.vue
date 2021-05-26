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
    <h1>Login <small v-text="intent" /></h1>
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
      <LoginForm />
    </section>
    <section
      class="section email"
    >
      <EmailLoginForm />
    </section>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
.message {
  margin: 2rem 0 2rem;
  padding: 1rem;
  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
}
</style>

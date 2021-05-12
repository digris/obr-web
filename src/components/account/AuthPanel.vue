<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';
import Modal from '@/components/UI/Modal.vue';
import SocialLogin from '@/components/account/SocialLogin.vue';
import LoginForm from '@/components/account/LoginForm.vue';
import EmailLoginForm from '@/components/account/EmailLoginForm.vue';

export default defineComponent({
  components: {
    Modal,
    SocialLogin,
    LoginForm,
    EmailLoginForm,
  },
  setup() {
    const store = useStore();
    const isVisible = ref(false);
    const next = ref(null);
    const close = () => {
      isVisible.value = false;
    };
    eventBus.on('account:authenticate', (event) => {
      isVisible.value = true;
      next.value = event.next || null;
    });
    store.watch((state: any) => state.account.currentUser, (newUser) => {
      if (newUser) {
        isVisible.value = false;
      }
    });
    return {
      close,
      isVisible,
      next,
    };
  },
});
</script>
<template>
  <Modal
    :is-visible="isVisible"
    @close="close"
  >
    <h1>Login</h1>
    <section
      class="section"
    >
      <SocialLogin
        :next="next"
      />
    </section>
    <section
      class="section"
    >
      <p>Oder anmelden mit:</p>
      <LoginForm />
    </section>
    <section
      class="section"
    >
      <EmailLoginForm />
    </section>
  </Modal>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
</style>

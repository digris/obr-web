<script lang="ts">
import { defineComponent, ref } from "vue";

import SocialLogin from "@/components/account/SocialLogin.vue";
import EmailLoginForm from "@/components/account/EmailLoginForm.vue";
import EmailLoginVerify from "@/components/account/EmailLoginVerify.vue";

export default defineComponent({
  components: {
    SocialLogin,
    EmailLoginForm,
    EmailLoginVerify,
  },
  props: {
    next: {
      type: [null, String],
      default: null,
    },
  },
  setup() {
    const socialLoginVisible = ref(true);
    const emailLoginVisible = ref(true);
    const emailLoginVerifyVisible = ref(false);
    const emailSentTo = ref("");
    const handleEmailSent = (email: string) => {
      emailSentTo.value = email;
      socialLoginVisible.value = false;
      emailLoginVisible.value = false;
      emailLoginVerifyVisible.value = true;
    };
    const reset = () => {
      emailSentTo.value = "";
      socialLoginVisible.value = true;
      emailLoginVisible.value = true;
      emailLoginVerifyVisible.value = false;
    };
    return {
      socialLoginVisible,
      emailLoginVisible,
      emailLoginVerifyVisible,
      handleEmailSent,
      emailSentTo,
      reset,
    };
  },
});
</script>
<template>
  <div class="auth-panel">
    <section v-if="socialLoginVisible" class="section social">
      <i18n-t keypath="account.auth.socialAccount" tag="p" />
      <SocialLogin :next="next" />
    </section>
    <div>
      <section v-if="emailLoginVisible" class="section email">
        <EmailLoginForm :next="next" @email-sent="handleEmailSent" />
      </section>
      <section v-if="emailLoginVerifyVisible" class="section email">
        <EmailLoginVerify :email="emailSentTo" @reset="reset" />
      </section>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
.auth-panel {
  display: flex;
  flex-direction: column;
  .subtitle {
    @include typo.large;
    display: flex;
    justify-content: flex-start;
  }
  .social {
    margin-top: 2rem;
    > p {
      margin-bottom: 1rem;
      @include responsive.bp-medium {
        @include typo.small;
      }
    }
  }
  .email {
    > p {
      margin-bottom: 0.5rem;
    }
  }
}
</style>

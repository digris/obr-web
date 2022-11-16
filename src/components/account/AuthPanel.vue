<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";
import SidePanel from "@/components/ui/panel/SidePanel.vue";

import SocialLogin from "@/components/account/SocialLogin.vue";
import EmailLoginForm from "@/components/account/EmailLoginForm.vue";
import EmailLoginVerify from "@/components/account/EmailLoginVerify.vue";

import ServiceInfoAside from "./context/ServiceInfoAside.vue";
import Availability from "./legal/Availability.vue";
import Terms from "./legal/Terms.vue";

export default defineComponent({
  components: {
    SidePanel,
    SocialLogin,
    EmailLoginForm,
    EmailLoginVerify,
    ServiceInfoAside,
    Availability,
    Terms,
  },
  setup() {
    const { user } = useAccount();
    const isVisible = ref(false);
    const socialLoginVisible = ref(true);
    const emailLoginVisible = ref(true);
    const emailLoginVerifyVisible = ref(false);
    const intent = ref("login");
    const next = ref(null);
    const message = ref(null);
    const emailSentTo = ref("");
    const close = () => {
      isVisible.value = false;
    };
    const setIntent = (value: string) => {
      intent.value = value;
    };
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
    eventBus.on("account:authenticate", (event) => {
      isVisible.value = true;
      if (event.intent) {
        intent.value = event.intent;
      }
      next.value = event.next || null;
      message.value = event.message || null;
    });
    watch(
      () => user.value,
      (newUser) => {
        if (newUser) {
          isVisible.value = false;
        }
      }
    );
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
      emailSentTo,
      reset,
    };
  },
});
</script>
<template>
  <SidePanel :is-visible="isVisible" @close="close">
    <div class="panel">
      <i18n-t keypath="account.auth.login" tag="div" class="title" />
      <div v-if="message" class="message">
        <p>{{ message }}</p>
      </div>
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
      <section class="section availability">
        <Availability />
      </section>
    </div>
    <template #footer>
      <Terms class="terms" />
    </template>
    <!-- NOTE: design to be discussed -->
    <template #aside>
      <ServiceInfoAside />
    </template>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
.panel {
  display: flex;
  min-height: 100%;
  overflow-y: scroll;
  flex-direction: column;
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
.section.availability {
  flex-grow: 1;
  padding-top: 1rem;
  align-items: center;
  display: flex;
  @include responsive.bp-medium {
    @include typo.small;
  }
}
.terms {
  @include responsive.bp-medium {
    @include typo.small;
    //padding-bottom: 1rem;
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

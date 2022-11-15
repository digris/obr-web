<script lang="ts">
import type { PropType } from "vue";
import type { User } from "@/typings/api";
import { defineComponent, ref } from "vue";
import { useIntervalFn } from "@vueuse/core";
import { getSignedLoginCredentials } from "@/api/account";
import QrcodeVue from "qrcode.vue";
import Section from "../settings/Section.vue";

export default defineComponent({
  props: {
    user: {
      type: Object as PropType<User>,
      required: true,
    },
  },
  components: {
    Section,
    QrcodeVue,
  },
  setup() {
    const signedLoginUrl = ref("");
    const size = 200;
    const loadCredentials = async () => {
      const response = await getSignedLoginCredentials();
      signedLoginUrl.value = response.signedLoginUrl;
    };
    useIntervalFn(
      async () => {
        await loadCredentials();
      },
      5 * 60 * 1000, // very 5 minute
      { immediateCallback: true }
    );
    return {
      signedLoginUrl,
      size,
    };
  },
});
</script>

<template>
  <Section class="qr-code-login" title="Mobile Login" :outlined="false">
    <div class="container">
      <div class="code">
        <qrcode-vue v-if="signedLoginUrl" class="qr-code" :value="signedLoginUrl" :size="size" level="H" />
      </div>
      <div class="body">
        <p>Scan the QR-Code with your mobile's camera to login.</p>
      </div>
    </div>
  </Section>
</template>

<style lang="scss" scoped>
.qr-code-login {
  .container {
    display: grid;
    grid-template-columns: 1fr 3fr;
    grid-gap: 1rem;
    margin-top: 0.5rem;
    .code {
      .qr-code {
        aspect-ratio: 1;
        min-width: 100%;
        height: 100% !important;
      }
    }
  }
}
</style>

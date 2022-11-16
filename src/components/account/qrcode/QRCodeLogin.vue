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
      5 * 60 * 1000, // every 5 minutes
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
    <div class="info">
      <p>Scan the QR-Code with your mobile's camera to login.</p>
    </div>
    <div class="code">
      <qrcode-vue v-if="signedLoginUrl" class="qr-code" :value="signedLoginUrl" :size="size" level="H" />
    </div>
  </Section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.qr-code-login {
  .info {
    padding: 0.5rem 2rem 1rem 0;
    opacity: 0.5;
  }
  .code {
    max-width: 240px;
    .qr-code {
      aspect-ratio: 1;
      min-width: 100%;
      height: 100% !important;
    }
  }
}
</style>

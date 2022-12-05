<script lang="ts">
import { useIntervalFn } from "@vueuse/core";
import QrcodeVue from "qrcode.vue";
import type { PropType } from "vue";
import { defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";

import { getSignedLoginCredentials } from "@/api/account";
import type { User } from "@/typings/api";

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
    const { t } = useI18n();
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
      t,
      signedLoginUrl,
      size,
    };
  },
});
</script>

<template>
  <Section class="qr-code-login" :title="t('account.qrcode.title')" :outlined="false">
    <div class="info">
      <p v-text="t('account.qrcode.info')" />
    </div>
    <div class="code">
      <qrcode-vue
        v-if="signedLoginUrl"
        class="qr-code"
        :value="signedLoginUrl"
        :size="size"
        level="H"
      />
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

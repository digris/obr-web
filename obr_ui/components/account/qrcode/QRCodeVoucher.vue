<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import QrcodeVue from "qrcode.vue";

import { useSettings } from "@/composables/settings";
import type { UserVoucher } from "@/typings/api";

export default defineComponent({
  props: {
    voucher: {
      type: Object as PropType<UserVoucher>,
      required: true,
    },
  },
  components: {
    QrcodeVue,
  },
  setup(props) {
    const { t } = useI18n();
    const { darkMode } = useSettings();
    const voucherUrl = computed(() => {
      return `https://openbroadcast.ch/#${props.voucher.codeDisplay}`;
    });
    const size = 200;
    const bg = "#ffffff00";
    const fg = computed(() => {
      return darkMode.value ? "#ffffff" : "#000000";
    });
    return {
      t,
      voucherUrl,
      size,
      fg,
      bg,
    };
  },
});
</script>

<template>
  <qrcode-vue
    class="qr-code"
    :value="voucherUrl"
    :size="size"
    :background="bg"
    :foreground="fg"
    level="H"
  />
</template>

<style lang="scss" scoped>
.qr-code {
  border: 0;
}
</style>

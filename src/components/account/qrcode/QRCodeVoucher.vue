<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import QrcodeVue from "qrcode.vue";

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
    const voucherUrl = computed(() => {
      return `http://mbp14.local:5000/#${props.voucher.codeDisplay}`;
    });
    const size = 200;
    const fg = "#ffffff";
    const bg = "#ffffff00";
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

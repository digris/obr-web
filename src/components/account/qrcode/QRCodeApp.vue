<script lang="ts">
import { computed, defineComponent } from "vue";
import QrcodeVue from "qrcode.vue";

import { useSettings } from "@/composables/settings";

const URL = "https://itunes.apple.com/app/urbanspoon/id1643695398";

export default defineComponent({
  components: {
    QrcodeVue,
  },
  setup() {
    const { darkMode } = useSettings();
    const url = URL;
    const size = 200;
    const bg = "#ffffff00";
    const fg = computed(() => {
      return darkMode.value ? "#ffffff" : "#000000";
    });
    return {
      url,
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
    :value="url"
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

<script lang="ts">
import { defineComponent, PropType, ref } from "vue";
import QrcodeVue from 'qrcode.vue'
import type { User } from "@/typings/api";

export default defineComponent({
  props: {
    user: {
      type: Object as PropType<User>,
      required: true,
    },
  },
  components: {
    QrcodeVue,
  },
  setup() {
    const value = ref('https://example.com');
    const size = 200;
    return {
      value,
      size,
    };
  },
});
</script>

<template>
  <div>
    <pre v-text="user.uid" />
    <qrcode-vue :value="value" :size="size" level="H"/>
  </div>
</template>

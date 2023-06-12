<script lang="ts" setup>
import Radio from "@/components/broadcast/radio/Radio.vue";
import RadioMobile from "@/components/broadcast/radio/RadioMobile.vue";
import { useDevice } from "@/composables/device";

const { isSmallScreen } = useDevice();
</script>

<template>
  <RadioMobile v-if="isSmallScreen" />
  <Radio v-else />
</template>

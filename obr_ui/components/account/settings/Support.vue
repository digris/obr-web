<script lang="ts">
import { defineComponent } from "vue";

import Section from "./Section.vue";

export default defineComponent({
  components: {
    Section,
  },
  props: {
    user: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <Section title="Support Info">
    <div>
      <pre
        style="user-select: text"
        v-text="{
          uid: user.uid,
        }"
      />
    </div>
  </Section>
</template>

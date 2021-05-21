<script lang="ts">
import { defineComponent, ref } from 'vue';
import eventBus from '@/eventBus';
import Modal from '@/components/ui/Modal.vue';

import SubscribeTrial from '@/components/subscription/SubscribeTrial.vue';
import SubscribePlan from '@/components/subscription/SubscribePlan.vue';

export default defineComponent({
  components: {
    Modal,
    SubscribeTrial,
    SubscribePlan,
  },
  setup() {
    const isVisible = ref(false);
    const intent = ref('plan');
    const close = () => {
      isVisible.value = false;
    };
    const setIntent = (value: string) => {
      intent.value = value;
    };
    eventBus.on('subscription:subscribe', (event) => {
      intent.value = event.intent;
      isVisible.value = true;
    });
    return {
      close,
      isVisible,
      intent,
      setIntent,
    };
  },
});
</script>

<template>
  <Modal
    :is-visible="isVisible"
    @close="close"
  >
    <template #title>
      Subscription
    </template>
    <div
      class="subscribe"
    >
      <section>
        <SubscribeTrial
          v-if="(intent === 'trial')"
        />
        <SubscribePlan
          v-if="(intent === 'plan')"
        />
      </section>
    </div>
    <template #footer>
      <div
        class="legal"
      >
        (( Legal shizzle... ))
      </div>
    </template>
  </Modal>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
@use "@/style/elements/button";
.section {
  @include section.default;
}
.button {
  @include button.default;
}
.subscribe {
  color: inherit;
}
.current-subscription {
  margin: 1rem 0;
  padding: 1rem;
  &.is-active {
    background: #55ff55;
  }
}
.legal {
  font-size: 90%;
  opacity: 0.5;
}
</style>

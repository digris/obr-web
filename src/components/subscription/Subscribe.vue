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
    const next = ref(null);
    const message = ref(null);
    const successVisible = ref(false);
    const close = () => {
      isVisible.value = false;
      successVisible.value = false;
    };
    const setIntent = (value: string) => {
      intent.value = value;
    };
    eventBus.on('subscription:subscribe', (event) => {
      console.debug('subscription:subscribe', event);
      isVisible.value = true;
      intent.value = event.intent;
      next.value = event.next || null;
      message.value = event.message || null;
    });
    const showSuccess = () => {
      successVisible.value = true;
    };
    return {
      close,
      isVisible,
      intent,
      setIntent,
      showSuccess,
      successVisible,
      next,
      message,
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
    <!--
    <div
      v-if="message"
      class="message"
    >
      <p>{{ message }}</p>
    </div>
    -->
    <nav
      class="subscribe-menu"
    >
      <div
        class="tab-item"
        @click="setIntent('trial')"
        :class="{'is-selected': (intent === 'trial')}"
      >
        <span>Trial</span>
      </div>
      <div
        class="tab-item"
        @click="setIntent('plan')"
        :class="{'is-selected': (intent === 'plan')}"
      >
        <span>Paid Plan</span>
      </div>
      <div
        class="tab-item tab-item--text"
        @click="setIntent('voucher')"
        :class="{'is-selected': (intent === 'voucher')}"
      >
        <span>Do you have a code / voucher?</span>
      </div>
    </nav>
    <div
      class="subscribe"
    >
      <section>
        <transition name="fade" mode="out-in" appear>
          <SubscribeTrial
            v-if="(intent === 'trial')"
            @subscription-created="showSuccess"
          />
          <SubscribePlan
            v-else-if="(intent === 'plan')"
            :next="next"
          />
        </transition>
      </section>
    </div>
    <template
      v-if="successVisible"
      #success
      :level="error"
    >
      <div
        class="subscribe-success"
      >
        <h1
          class="title"
        >Your Plan has been updated</h1>
        <p
          class="message"
        >
          In cases like above, when only the default slot is provided content,
          the component's tags can be used as the slot's template.
        </p>
        <div
          class="cta"
        >
          <button
            @click.prevent="close"
            class="button"
          >Let's start exploring!</button>
        </div>
      </div>
    </template>
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
@use "@/style/elements/tab-menu";
.section {
  @include section.default;
}
.button {
  @include button.default;
}
.subscribe-menu {
  @include tab-menu.default
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
.subscribe-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  .title {
    font-size: 3rem;
    text-align: center;
  }
  .message {
    max-width: 75%;
    padding: 1.5rem 0 2rem;
    font-size: 1.75rem;
    line-height: 130%;
    text-align: center;
  }
  .cta {
    .button {
      @include button.default(4rem);
    }
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 100ms;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

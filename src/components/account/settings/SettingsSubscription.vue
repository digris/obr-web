<script lang="ts">
import { computed, defineComponent, onMounted } from 'vue';
import eventBus from '@/eventBus';
import CurrentSubscription from '@/components/subscription/CurrentSubscription.vue';

export default defineComponent({
  components: {
    CurrentSubscription,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const subscription = computed(() => props.user.subscription);
    console.debug('subscription', subscription);
    const subscribe = (intent: string) => {
      const event = {
        intent,
        next: window.location.pathname,
      };
      eventBus.emit('subscription:subscribe', event);
    };
    onMounted(() => {
      // NOTE: just testing - initially show trial CTA if no subscription yet.
      if (!subscription.value) {
        subscribe('trial');
      }
    });
    return {
      subscription,
      subscribe,
    };
  },
});
</script>

<template>
  <div
    class="subscription"
  >
    <div
      v-if="subscription"
    >
      <CurrentSubscription />
    </div>
    <div
      v-else
    >
      <div
        class="lead">
        <p>
          Keine Abos - dafür Prepaid Guthaben!
          <br>
          Die von uns gespielten Inhalte zu jederzeit hören für CHF 1.– pro Monat.
        </p>
      </div>
      <p>
        <span
          @click="subscribe('plan')"
          class="cta"
        >
          Los!
        </span>
      </p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/button";
.subscription {
  .lead {
    @include typo.large;
    padding-bottom: 1rem;
  }
  .cta {
    @include button.default(2.5rem);
    max-width: 33%;
  }
}
</style>

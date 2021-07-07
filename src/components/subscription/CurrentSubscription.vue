<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';

import eventBus from '@/eventBus';
import Datetime from '@/components/ui/date/Datetime.vue';

export default defineComponent({
  components: {
    Datetime,
  },
  setup() {
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    const now = ref(DateTime.now());
    const subscription = computed(() => {
      return (currentUser.value) ? currentUser.value.subscription : null;
    });
    const numDaysRemaining = computed(() => {
      if (!subscription.value) {
        return null;
      }
      const activeUntil = DateTime.fromISO(subscription.value.activeUntil);
      const diff = activeUntil.diff(now.value, ['days']);
      return Math.round(diff.days);
    });
    const isActive = computed(() => (subscription.value && subscription.value.isActive));
    const title = computed(() => {
      if (isActive.value) {
        return 'Active Subscription';
      }
      return 'Guthaben abgelaufen';
    });
    const extendSubscription = () => {
      const event = {
        intent: 'plan',
      };
      eventBus.emit('subscription:subscribe', event);
    };
    return {
      currentUser,
      subscription,
      isActive,
      numDaysRemaining,
      title,
      extendSubscription,
    };
  },
});
</script>

<template>
  <div
    class="subscription"
    :class="{'is-active': isActive, 'is-expired': !isActive}"
  >
    <div
      class="details"
    >
      <p
        v-text="title"
      />
      <p>
        {{ numDaysRemaining }} Tage
      </p>
      <p>
        Gültig bis am:
        <Datetime
          :value="subscription.activeUntil"
          :display-time="(false)"
        />
      </p>
    </div>
    <div
      class="actions"
    >
      <button
        @click="extendSubscription"
        class="button"
      >
        Guthaben laden
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/button";
.subscription {
  display: grid;
  grid-template-columns: 1fr auto;
  color: rgb(var(--c-black));
  &.is-active {
    color: rgb(var(--c-success));
  }
  &.is-expired {
    color: rgb(var(--c-warning));
  }
  .details {
    @include typo.large;
  }
  .actions {
    align-self: end;
    padding-top: 0.5rem;
    .button {
      @include button.default;
    }
  }
}
</style>

<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useAccount } from "@/composables/account";
import { DateTime } from "luxon";

import eventBus from "@/eventBus";
import Datetime from "@/components/ui/date/Datetime.vue";

export default defineComponent({
  components: {
    Datetime,
  },
  setup() {
    const { subscription } = useAccount();
    const now = ref(DateTime.now());
    const numDaysRemaining = computed(() => {
      if (!subscription.value) {
        return null;
      }
      const activeUntil = DateTime.fromISO(subscription.value.activeUntil);
      const diff = activeUntil.diff(now.value, ["days"]);
      return Math.round(diff.days);
    });
    const isActive = computed(() => subscription.value && subscription.value.isActive);
    const isBlocked = computed(() => subscription.value && subscription.value.isBlocked != false);
    // const blockedReason = computed(() => subscription.value && subscription.value.isBlocked || null);
    const title = computed(() => {
      if (isActive.value) {
        return "Guthaben";
      }
      return "Guthaben abgelaufen";
    });
    const extendSubscription = () => {
      if (isBlocked.value) {
        return;
      }
      const event = {
        intent: "plan",
      };
      eventBus.emit("subscription:subscribe", event);
    };
    return {
      subscription,
      isActive,
      isBlocked,
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
    @click.stop="extendSubscription"
    :class="{
      'is-active': isActive,
      'is-blocked': isBlocked,
      'is-expired': !isActive,
    }"
  >
    <div v-if="isBlocked" class="details">
      NOTE: Currently we can only provide access to our on-demand service for people living in
      Switzerland.
    </div>
    <div v-else class="details">
      <p v-text="title" />
      <p>{{ numDaysRemaining }} Tage</p>
      <p>
        Gültig bis am:
        <Datetime :value="subscription.activeUntil" :display-time="false" />
      </p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.subscription {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto;
  color: rgb(var(--c-black));
  cursor: pointer;
  &.is-active {
    color: rgb(var(--c-green));
  }
  &.is-expired {
    color: rgb(var(--c-red));
  }
  &.is-blocked {
    color: rgb(var(--c-red));
  }
  /*
  .details {
    @include typo.large;
  }
  */
}
</style>

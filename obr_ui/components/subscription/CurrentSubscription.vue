<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { DateTime } from "luxon";

import Datetime from "@/components/ui/date/Datetime.vue";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

export default defineComponent({
  components: {
    Datetime,
  },
  setup() {
    const { subscription } = useAccount();
    const faqLink = "/faq/#42C745E4";
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
    const extendSubscription = () => {
      if (isBlocked.value) {
        return;
      }
      const event = {
        intent: "voucher",
      };
      eventBus.emit("subscription:subscribe", event);
    };
    return {
      subscription,
      faqLink,
      isActive,
      isBlocked,
      numDaysRemaining,
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
      <i18n-t keypath="geolocation.availability.note" />
    </div>
    <div v-else-if="!isActive" class="details">
      <!-- NOTE: temporary text as long as subscription is not possible
      <i18n-t v-if="!isActive" keypath="subscription.creditsExpired" tag="p" />
      -->
      <i18n-t keypath="subscription.noCredits" tag="p" />
      <i18n-t keypath="subscription.noCreditsNote" tag="p" class="note" />
    </div>
    <div v-else class="details">
      <i18n-t keypath="subscription.validNumDays" tag="p" :plural="numDaysRemaining" />
      <i18n-t v-if="subscription" keypath="subscription.validUntilDate" tag="p">
        <Datetime :value="subscription.activeUntil" :display-time="false" />
      </i18n-t>
    </div>
    <div v-if="!isBlocked" class="actions">
      <i18n-t
        @click="extendSubscription"
        keypath="subscription.voucher.redeemCode"
        tag="button"
        class="button"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/button";

.subscription {
  position: relative;
  display: grid;
  grid-template-rows: 1fr auto;
  color: rgb(var(--c-dark));
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

  .details {
    .note {
      @include typo.default;

      color: rgb(var(--c-dark) / 50%);
      white-space: pre-line;
    }
  }

  .actions {
    @include typo.default;

    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: center;

    .button {
      @include button.outlined(2.5rem);

      min-width: 33%;
    }
  }
}
</style>

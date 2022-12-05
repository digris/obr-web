<script lang="ts">
import { DateTime } from "luxon";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconAlert from "@/components/ui/icon/IconAlert.vue";
import { useAccount } from "@/composables/account";

export default defineComponent({
  components: {
    CircleButton,
    IconAlert,
  },
  setup() {
    const { t } = useI18n();
    const { subscription } = useAccount();
    const now = DateTime.now();
    const numDaysRemaining = computed(() => {
      if (!subscription.value) {
        return null;
      }
      const activeUntil = DateTime.fromISO(subscription.value.activeUntil);
      const diff = activeUntil.diff(now, ["days"]);
      return Math.round(diff.days);
    });
    const isActive = computed(() => subscription.value && subscription.value.isActive);
    const isBlocked = computed(() => subscription.value && subscription.value.isBlocked != false);
    return {
      t,
      subscription,
      isActive,
      isBlocked,
      numDaysRemaining,
    };
  },
});
</script>

<template>
  <div>
    <div v-if="subscription" class="subscription-status">
      <router-link
        :to="{ name: 'accountSettings' }"
        class="status"
        :class="{
          'is-active': isActive,
          'is-expired': !isActive,
        }"
      >
        <div v-if="!isActive || isBlocked" class="icon-alert">
          <CircleButton>
            <IconAlert :scale="0.8" />
          </CircleButton>
        </div>
        <div v-else>
          <span> Free access </span>
          <br />
          <span v-text="t('subscription.numDaysRemaining', numDaysRemaining)" />
        </div>
      </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.subscription-status {
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;

  .status {
    @include typo.tiny;
    @include typo.uppercase;

    height: 100%;
    width: 100%;
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    line-height: 14px;

    /*
    &.is-expired {
      color: rgb(var(--c-warning));
    }
    */
  }
}
</style>

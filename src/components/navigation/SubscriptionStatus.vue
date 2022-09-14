<script lang="ts">
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import { DateTime } from "luxon";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconAlert from "@/components/ui/icon/IconAlert.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconAlert,
  },
  setup() {
    const { t } = useI18n();
    const store = useStore();
    const subscription = computed(() => store.getters["account/subscription"]);
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
    return {
      t,
      subscription,
      isActive,
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
        <div v-if="isActive">
          <span> Free access </span>
          <br />
          <span v-text="t('subscription.numDaysRemaining', numDaysRemaining)" />
        </div>
        <div v-else class="icon-alert">
          <CircleButton>
            <IconAlert :scale="0.8" />
          </CircleButton>
        </div>
      </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.subscription-status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  .status {
    @include typo.tiny;
    @include typo.uppercase;
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    width: 100%;
    height: 100%;
    line-height: 14px;
    /*
    &.is-expired {
      color: rgb(var(--c-warning));
    }
    */
  }
}
</style>

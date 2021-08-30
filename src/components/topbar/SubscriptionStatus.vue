<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { DateTime } from 'luxon';

import Datetime from '@/components/ui/date/Datetime.vue';

export default defineComponent({
  components: {
    Datetime,
  },
  setup() {
    const detailsVisible = ref(false);
    const store = useStore();
    const subscription = computed(() => store.getters['account/subscription']);
    const now = ref(DateTime.now());
    const numDaysRemaining = computed(() => {
      if (!subscription.value) {
        return null;
      }
      const activeUntil = DateTime.fromISO(subscription.value.activeUntil);
      const diff = activeUntil.diff(now.value, ['days']);
      return Math.round(diff.days);
    });
    const isActive = computed(() => (subscription.value && subscription.value.isActive));
    const showDetails = () => {
      detailsVisible.value = true;
    };
    const hideDetails = () => {
      detailsVisible.value = false;
    };
    return {
      subscription,
      isActive,
      numDaysRemaining,
      detailsVisible,
      showDetails,
      hideDetails,
    };
  },
});
</script>

<template>
  <div>
    <div
      v-if="subscription"
      @mouseenter="showDetails"
      @mouseleave="hideDetails"
      class="subscription-status"
    >
      <router-link
        :to="{ name: 'accountSettings' }"
        class="status"
        :class="{'is-active': isActive, 'is-expired': !isActive}"
      >
        <span
          v-if="isActive"
        >
          <span
            v-text="numDaysRemaining"
          />
          Tage
        </span>
        <span
          v-else
        >
          <span
            v-text="numDaysRemaining"
          />
          Tage
        </span>
      </router-link>
      <div
        v-if="(subscription && detailsVisible)"
        class="subscription"
        :class="{'is-active': isActive, 'is-expired': !isActive}"
      >
        <div
          class="title"
        >
          <span>Guthaben</span>
        </div>
        <div
          class="details"
        >
          <span
            v-if="isActive"
          >
            Gültig bis:
            <Datetime
              :value="subscription.activeUntil"
            />
          </span>
          <span
            v-else
          >
            Abgelaufen:
            <Datetime
              :value="subscription.activeUntil"
            />
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.subscription-status {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  .status {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    &.is-active {
      color: rgb(var(--c-success));
    }
    &.is-expired {
      color: rgb(var(--c-warning));
    }
  }
  .subscription {
    position: absolute;
    top: 54px;
    min-width: 240px;
    padding: 1rem;
    color: rgb(var(--c-black));
    background: rgb(var(--c-white));
    &.is-active {
      background: rgb(var(--c-success));
    }
    &.is-expired {
      background: rgb(var(--c-warning));
    }
    .title {
      margin-bottom: 0.5rem;
    }
    .details {
      padding-top: 0.5rem;
      border-top: 1px solid rgb(var(--c-black));
    }
  }
}
</style>

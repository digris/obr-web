<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';

import Datetime from '@/components/ui/Datetime.vue';

export default defineComponent({
  components: {
    Datetime,
  },
  setup() {
    const detailsVisible = ref(false);
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    // eslint-disable-next-line arrow-body-style
    const subscription = computed(() => {
      return (currentUser.value) ? currentUser.value.subscription : null;
    });

    const isActive = computed(() => (subscription.value && subscription.value.isActive));
    const showDetails = () => {
      detailsVisible.value = true;
    };
    const hideDetails = () => {
      detailsVisible.value = false;
    };
    return {
      currentUser,
      subscription,
      isActive,
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
      v-if="currentUser"
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
          +
        </span>
        <span
          v-else
        >
          -
        </span>
      </router-link>
      <div
        v-if="(subscription && currentUser && detailsVisible)"
        class="subscription"
        :class="{'is-active': isActive, 'is-expired': !isActive}"
      >
        <div
          class="title"
        >
          <span>Subscription</span>
          <span
            v-if="subscription.isTrial"
          >
            (Trial)
          </span>
        </div>
        <div
          class="details"
        >
          <span
            v-if="isActive"
          >
            Active until:
            <Datetime
              :value="subscription.activeUntil"
            />
          </span>
          <span
            v-else
          >
            Expired:
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
    top: 72px;
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

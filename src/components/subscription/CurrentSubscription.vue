<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

import eventBus from '@/eventBus';
import Datetime from '@/components/ui/Datetime.vue';

export default defineComponent({
  components: {
    Datetime,
  },
  setup() {
    const store = useStore();
    const currentUser = computed(() => store.getters['account/currentUser']);
    // eslint-disable-next-line arrow-body-style
    const subscription = computed(() => {
      return (currentUser.value) ? currentUser.value.subscription : null;
    });
    const isActive = computed(() => (subscription.value && subscription.value.isActive));
    const title = computed(() => {
      if (isActive.value) {
        return 'Active Subscription';
      }
      return 'Expired Subscription';
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
      class="title"
    >
      <h2>
        {{ title }}
      </h2>
    </div>
    <div
      class="details"
    >
      <div
        class="label"
      >
        ID:
      </div>
      <div
        class="value"
        v-text="subscription.uid"
      />
      <div
        class="label"
      >
        Expires:
      </div>
      <div
        class="value"
      >
        <Datetime
          :value="subscription.activeUntil"
          :display-time="(false)"
        />
      </div>
    </div>
    <div
      class="actions"
    >
      <button
        @click="extendSubscription"
        class="button"
      >
        Extend subscription
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";
@use "@/style/elements/info-grid";
.subscription {
  display: grid;
  grid-template-areas:
    "title actions"
    "details actions";
  grid-template-columns: 1fr auto;
  padding: 1rem;
  color: rgb(var(--c-black));
  &.is-active {
    background: rgb(var(--c-success));
  }
  &.is-expired {
    background: rgb(var(--c-warning));
  }
  .title {
    grid-area: title;
    margin-bottom: 1rem;
  }
  .details {
    @include info-grid.default;
    grid-area: details;
  }
  .actions {
    grid-area: actions;
    align-self: end;
    padding-top: 0.5rem;
    .button {
      @include button.default;
    }
  }
}
</style>

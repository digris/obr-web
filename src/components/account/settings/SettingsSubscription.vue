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
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus lobortis rhoncus nisl.
          Quisque luctus mattis lectus.
          <br>
          Proin mi ante, auctor molestie consectetur at.
        </p>
      </div>
      <div
        class="subscription__options"
      >
        <div
          @click="subscribe('trial')"
          class="subscription__option"
        >
          <h2
            class="title"
          >
            Start 14 day FREE trial
          </h2>
          <p
            class="description"
          >
            No credit-card required
          </p>
          <div
            class="cta"
          >
            <button
              class="button button--cta"
            >
              Los
            </button>
          </div>
        </div>
        <div
          @click="subscribe('plan')"
          class="subscription__option"
        >
          <h2
            class="title"
          >
            Get a Prepaid Plan
          </h2>
          <p
            class="description"
          >
            CHF 1.-
          </p>
          <div
            class="cta"
          >
            <button
              class="button button--cta"
            >
              Los
            </button>
          </div>
        </div>
        <div
          @click="subscribe('voucher')"
          class="subscription__option"
        >
          <h2
            class="title"
          >
            Redeem voucher
          </h2>
          <p
            class="description"
          >
            Haz got code?
          </p>
          <div
            class="cta"
          >
            <button
              class="button button--cta"
            >
              Los
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/button";
@mixin option {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: rgb(var(--c-black));
  background: rgba(var(--c-white), 1);
  transition: background 100ms;
  &:hover {
    background: rgba(var(--c-cta), 1);
  }
  .title {
    font-size: 120%;
  }
  .description {
    padding: 0.5rem 0;
    font-size: 90%;
  }
  .cta {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding-top: 0.5rem;
    .button {
      @include button.default;
      min-width: 75%;
      height: 2rem;
      min-height: unset;
      //background: rgb(var(--c-cta));
    }
  }
}
.subscription {
  .lead {
    padding: 1rem 0;
    line-height: 140%;
  }
  &__options {
    display: grid;
    grid-gap: 0.5rem;
    grid-template-columns: repeat(3, 1fr);
    @include responsive.bp-small {
      grid-template-columns: unset;
    }
  }
  &__option {
    padding: 1rem;
    cursor: pointer;
    @include option;
  }
}
</style>

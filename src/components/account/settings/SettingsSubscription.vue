<script lang="ts">
import { computed, defineComponent } from 'vue';
import eventBus from '@/eventBus';
import CurrentSubscription from '@/components/subscription/CurrentSubscription.vue';
import Subscribe from '@/components/subscription/Subscribe.vue';

export default defineComponent({
  components: {
    CurrentSubscription,
    Subscribe,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const subscription = computed(() => props.user.subscription);
    const subscribe = (intent: string) => {
      const event = {
        intent,
        next: window.location.pathname,
      };
      eventBus.emit('subscription:subscribe', event);
    };
    return {
      subscription,
      subscribe,
    };
  },
});
</script>

<template>
  <div>
    <Subscribe />
  </div>
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
          Quisque luctus mattis lectus, non faucibus purus volutpat volutpat. Suspendisse posuere
          diam a tincidunt venenatis. Quisque eget erat tempor libero dignissim venenatis.
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
    padding: 1rem 0.5rem;
  }
  &__options {
    display: grid;
    grid-gap: 0.5rem;
    grid-template-columns: repeat(3, 1fr);
  }
  &__option {
    padding: 1rem;
    cursor: pointer;
    @include option;
  }
}
</style>

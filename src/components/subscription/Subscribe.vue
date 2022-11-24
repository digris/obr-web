<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import eventBus from "@/eventBus";
import { useNotification } from "@/composables/notification";
import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";

import SubscribePlan from "@/components/subscription/SubscribePlan.vue";
import SubscribeVoucher from "@/components/subscription/SubscribeVoucher.vue";

export default defineComponent({
  components: {
    OverlayPanel,
    SubscribePlan,
    SubscribeVoucher,
  },
  setup() {
    const router = useRouter();
    const { notify } = useNotification();
    const isVisible = ref(false);
    const intent = ref("plan");
    const next = ref(null);
    const message = ref(null);
    const successVisible = ref(false);
    const close = () => {
      isVisible.value = false;
      successVisible.value = false;
    };
    const setIntent = (value: string) => {
      intent.value = value;
    };
    eventBus.on("subscription:subscribe", (event) => {
      console.debug("subscription:subscribe", event);
      isVisible.value = true;
      intent.value = event.intent;
      next.value = event.next || null;
      message.value = event.message || null;
    });
    const subscriptionUpdated = () => {
      console.debug("show success");
      // successVisible.value = true;
      close();
      notify({
        level: "success",
        body: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
      });
      if (next.value) {
        // @ts-ignore
        router.push(next.value);
      }
      console.debug("next:", next.value);
    };
    return {
      close,
      isVisible,
      intent,
      setIntent,
      subscriptionUpdated,
      successVisible,
      next,
      message,
    };
  },
});
</script>

<template>
  <OverlayPanel :is-visible="isVisible" @close="close">
    <div>
      <div class="title">Guthaben</div>
      <p class="lead">
        Keine Abos - dafür Prepaid Guthaben!
        <br />
        Die von uns gespielten Inhalte zu jederzeit hören für CHF 1.– pro Monat.
      </p>
      <p>&nbsp;</p>
      <p v-if="intent === 'plan'" class="lead">
        Hast du einen <a @click.prevent="setIntent('voucher')">Gratis-Code</a>?
      </p>
      <p v-if="intent === 'voucher'" class="lead">
        Du hast keinen Code?
        <a @click.prevent="setIntent('plan')">Guthaben kaufen</a>.
      </p>
    </div>
    <div class="subscribe">
      <section>
        <transition name="fade" mode="out-in" appear>
          <SubscribePlan v-if="intent === 'plan'" :next="next" />
          <SubscribeVoucher
            v-else-if="intent === 'voucher'"
            :next="next"
            @subscription-extended="subscriptionUpdated"
          />
        </transition>
      </section>
    </div>
    <template v-if="successVisible" #success>
      <div class="subscribe-success">
        <h1 class="title">Your Plan has been updated</h1>
        <p class="message">(( message ))</p>
        <div class="cta">
          <button @click.prevent="close" class="button">Let's start exploring!</button>
        </div>
      </div>
    </template>
    <template #footer>
      <!--
      <div class="legal">(( Legal shizzle... ))</div>
      -->
    </template>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/section";
@use "@/style/elements/button";
@use "@/style/elements/tab-menu";
.section {
  @include section.default;
}
.button {
  @include button.default;
}
.subscribe-menu {
  @include tab-menu.default;
}
.current-subscription-text {
  margin: 2rem 0;
}
.title {
  @include typo.x-large;
  @include typo.bold;
}
.lead {
  @include typo.large;
  a {
    text-decoration: underline;
    cursor: pointer;
  }
}
.subscribe {
  color: inherit;
}
.current-subscription {
  margin: 1rem 0;
  padding: 1rem;
}
.legal {
  font-size: 90%;
  opacity: 0.5;
}
.subscribe-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  .title {
    font-size: 3rem;
    text-align: center;
  }
  .message {
    max-width: 75%;
    padding: 1.5rem 0 2rem;
    font-size: 1.75rem;
    line-height: 130%;
    text-align: center;
  }
  .cta {
    .button {
      @include button.default(4rem);
    }
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 100ms;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

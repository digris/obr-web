<script lang="ts">
import { defineComponent, ref, watch } from "vue";

import AuthPanel from "@/components/account/AuthPanel.vue";
import SidePanel from "@/components/ui/panel/SidePanel.vue";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

import ServiceInfoAside from "./context/ServiceInfoAside.vue";
import Availability from "./legal/Availability.vue";
import Terms from "./legal/Terms.vue";

export default defineComponent({
  components: {
    SidePanel,
    AuthPanel,
    ServiceInfoAside,
    Availability,
    Terms,
  },
  setup() {
    const { user } = useAccount();
    const isVisible = ref(false);
    const next = ref(null);
    const close = () => (isVisible.value = false);
    eventBus.on("account:authenticate", (event) => {
      isVisible.value = true;
      next.value = event.next || null;
    });
    watch(
      () => user.value,
      (newUser) => {
        if (newUser) {
          isVisible.value = false;
        }
      }
    );
    return {
      close,
      isVisible,
      next,
    };
  },
});
</script>
<template>
  <SidePanel :is-visible="isVisible" @close="close">
    <i18n-t keypath="account.auth.login" tag="div" class="title" />
    <AuthPanel :next="next" />
    <template #footer>
      <section class="section availability">
        <Availability />
      </section>
      <Terms class="terms" />
    </template>
    <template #aside>
      <ServiceInfoAside />
    </template>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";

.title {
  @include typo.x-large;
  @include typo.bold;

  display: flex;
  justify-content: flex-start;
}

.auth-panel {
  overflow-y: auto;

  @include responsive.bp-medium {
    min-height: 100%;
    margin-bottom: 4rem;
  }
}

.section.availability {
  flex-grow: 1;
  padding-bottom: 1rem;
  align-items: center;
  display: flex;
  @include responsive.bp-medium {
    @include typo.small;
  }
}

.terms {
  @include responsive.bp-medium {
    @include typo.small;
  }
}

.lead {
  @include typo.large;

  a {
    text-decoration: underline;
    cursor: pointer;
  }
}

.message {
  margin: 1rem 0;
  padding: 1rem;
  background: rgb(var(--c-cta) / 10%);
  border-left: 4px solid rgb(var(--c-cta));
}
</style>

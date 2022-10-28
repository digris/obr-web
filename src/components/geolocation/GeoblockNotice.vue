<script lang="ts">
import { defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";
import eventBus from "@/eventBus";
import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";

export default defineComponent({
  components: {
    OverlayPanel,
  },
  setup() {
    const { t } = useI18n();
    const isVisible = ref(false);
    const message = ref(null);
    const successVisible = ref(false);
    const close = () => {
      isVisible.value = false;
      successVisible.value = false;
    };
    eventBus.on("geolocation:blocked", (event) => {
      console.debug("geolocation:blocked", event);
      isVisible.value = true;
      message.value = event.message || null;
    });
    return {
      t,
      close,
      isVisible,
      message,
    };
  },
});
</script>

<template>
  <OverlayPanel :is-visible="isVisible" @close="close">
    <div>
      <div class="title">Sorry</div>
      <div class="availability">
        <i18n-t keypath="geolocation.availability.note" tag="p" class="note" />
        <i18n-t keypath="geolocation.availability.faqNote" tag="p" class="faq-note">
          <router-link to="/faq/" v-text="t('geolocation.availability.faqLabel')" />
        </i18n-t>
      </div>
    </div>
    <template #footer>
      <p v-text="message" />
    </template>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/section";
.section {
  @include section.default;
}
.current-subscription-text {
  margin: 2rem 0;
}
.title {
  @include typo.x-large;
  @include typo.bold;
}
.note {
  @include typo.large;
  a {
    text-decoration: underline;
    cursor: pointer;
  }
}
.faq-note {
  margin-top: 1rem;
  a {
    text-decoration: underline;
    cursor: pointer;
  }
}
.legal {
  font-size: 90%;
  opacity: 0.5;
}
</style>

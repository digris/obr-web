<script lang="ts">
import { defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import Section from "./Section.vue";

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
  },
  props: {
    user: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  emits: ["updated"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const newsletters = ref([
      {
        channel: "foo",
        subscribed: true,
        title: "Open Broadcast Newsletter",
      },
      {
        channel: "bar",
        subscribed: false,
        title: "Wochenprogramm",
      },
      {
        channel: "baz",
        subscribed: true,
        title: "Sendetips",
      },
    ]);
    const formVisible = ref(false);
    const showForm = () => {
      formVisible.value = true;
    };
    const hideForm = async () => {
      formVisible.value = false;
    };
    const onUpdated = async () => {
      await hideForm();
      emit("updated");
    };
    const onEdit = () => {
      showForm();
    };
    return {
      t,
      newsletters,
      onEdit,
      formVisible,
      hideForm,
      onUpdated,
    };
  },
});
</script>

<template>
  <Section :title="t('account.settings.newsletter.title')" @edit="onEdit">
    <div v-for="newsletter in newsletters" :key="newsletter.channel" class="newsletter">
      <div>
        <span v-if="newsletter.subscribed">&#9679;</span>
        <span v-else>&#9675;</span>
      </div>
      <div>
        <div v-text="newsletter.title"></div>
      </div>
    </div>
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    :title="t('account.settings.newsletter.title')"
  >
    <div>(( Newsletter Form ))</div>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.newsletter {
  display: flex;
  gap: 1rem;
  //padding: 0.25rem;
}
</style>

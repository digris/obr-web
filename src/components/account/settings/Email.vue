<script lang="ts">
import { ref, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import Section from "./Section.vue";
import Form from "./EmailForm.vue";

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
    Form,
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
      onEdit,
      formVisible,
      hideForm,
      onUpdated,
    };
  },
});
</script>

<template>
  <Section :title="t('account.settings.email.title')" @edit="onEdit">
    <p v-text="user.email" />
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    :title="t('account.settings.email.title')"
  >
    <Form :current-email="user.email" @updated="onUpdated" />
  </OverlayPanel>
</template>

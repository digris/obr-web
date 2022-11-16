<script lang="ts">
import { ref, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import Section from "./Section.vue";
import Form from "./PasswordForm.vue";

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
    Form,
  },
  setup() {
    const { t } = useI18n();
    const formVisible = ref(false);
    const showForm = () => {
      formVisible.value = true;
    };
    const hideForm = () => {
      formVisible.value = false;
    };
    const onEdit = () => {
      showForm();
    };
    return {
      t,
      onEdit,
      formVisible,
      hideForm,
    };
  },
});
</script>

<template>
  <Section :title="t('account.settings.password.title')" @edit="onEdit">
    <p class="user-details" v-text="`●●●●●●●●`" />
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    :title="t('account.settings.password.title')"
  >
    <Form @updated="hideForm" />
  </OverlayPanel>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";

import Form from "./AddressForm.vue";
import Section from "./Section.vue";

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
    Form,
  },
  props: {
    address: {
      type: Object,
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
  <Section :title="t('account.settings.address.title')" @edit="onEdit">
    <div v-if="address">
      <p v-if="address.line1" v-text="address.line1" />
      <p v-if="address.line2" v-text="address.line2" />
      <p>
        <span
          v-if="address.country"
          v-text="`${address.country}${address.postalCode ? '-' : ''}`"
        />
        <span
          v-if="address.postalCode"
          v-text="`${address.postalCode}${address.country ? ' ' : ''}`"
        />
        <span v-if="address.city" v-text="address.city" />
      </p>
    </div>
    <p v-else v-text="`---`" />
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    :title="t('account.settings.address.title')"
  >
    <Form :address="address || {}" @updated="onUpdated" />
  </OverlayPanel>
</template>

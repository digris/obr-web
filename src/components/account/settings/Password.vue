<script lang="ts">
import {
  ref,
  defineComponent,
} from 'vue';

import OverlayPanel from '@/components/ui/panel/OverlayPanel.vue';
import Section from './Section.vue';
import Form from './PasswordForm.vue';

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
    Form,
  },
  setup() {
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
      onEdit,
      formVisible,
      hideForm,
    };
  },
});
</script>

<template>
  <Section
    title="Passwort"
    @edit="onEdit"
  >
    <p
      class="user-details"
      v-text="`●●●●●●●●`"
    />
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    title="Passwort"
  >
    <Form
      @updated="hideForm"
    />
  </OverlayPanel>
</template>

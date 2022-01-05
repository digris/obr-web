<script lang="ts">
import {
  ref,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

import OverlayPanel from '@/components/ui/panel/OverlayPanel.vue';
import Section from './Section.vue';
import Form from './EmailForm.vue';

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
  setup() {
    const store = useStore();
    const formVisible = ref(false);
    const showForm = () => {
      formVisible.value = true;
    };
    const hideForm = async () => {
      formVisible.value = false;
    };
    const onUpdated = async () => {
      await store.dispatch('account/getUser');
      await hideForm();
    };
    const onEdit = () => {
      showForm();
    };
    return {
      onEdit,
      formVisible,
      hideForm,
      onUpdated,
    };
  },
});
</script>

<template>
  <Section
    title="E-Mail"
    @edit="onEdit"
  >
    <p
      class="user-details"
      v-text="user.email"
    />
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    title="E-Mail"
  >
    <Form
      :current-email="user.email"
      @updated="onUpdated"
    />
  </OverlayPanel>
</template>

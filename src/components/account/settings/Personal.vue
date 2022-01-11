<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
} from 'vue';

import OverlayPanel from '@/components/ui/panel/OverlayPanel.vue';
import Section from './Section.vue';
import Form from './PersonalForm.vue';

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
  emits: [
    'updated',
  ],
  setup(props, { emit }) {
    const fullName = computed(() => {
      if (props.user?.firstName && props.user?.lastName) {
        return `${props.user.firstName} ${props.user.lastName}`;
      }
      if (props.user?.firstName) {
        return props.user.firstName;
      }
      if (props.user?.lastName) {
        return props.user.lastName;
      }
      return null;
    });
    const formVisible = ref(false);
    const showForm = () => {
      formVisible.value = true;
    };
    const hideForm = async () => {
      formVisible.value = false;
    };
    const onUpdated = async () => {
      await hideForm();
      emit('updated');
    };
    const onEdit = () => {
      showForm();
    };
    return {
      fullName,
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
    title="Persönliche Angaben"
    @edit="onEdit"
  >
    <p
      v-if="fullName"
      v-text="fullName"
    />
    <p
      v-else
      v-text="`---`"
    />
  </Section>
  <OverlayPanel
    :is-visible="formVisible"
    @close="hideForm"
    title="Persönliche Angaben"
  >
    <Form
      :user="user"
      @updated="onUpdated"
    />
  </OverlayPanel>
</template>

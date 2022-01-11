<script lang="ts">
import {
  defineComponent,
} from 'vue';

import Section from './Section.vue';
import CurrentSubscription from '@/components/subscription/CurrentSubscription.vue';

export default defineComponent({
  components: {
    Section,
    CurrentSubscription,
  },
  emits: [
    'updated',
  ],
  setup(props, { emit }) {
    const onUpdated = async () => {
      emit('updated');
    };
    const onEdit = () => {
      console.debug('onEdit');
    };
    return {
      onEdit,
      onUpdated,
    };
  },
});
</script>

<template>
  <Section
    title="Guthaben für kostenpflichtige Inhalte"
    @edit="onEdit"
  >
    <CurrentSubscription />
  </Section>
</template>

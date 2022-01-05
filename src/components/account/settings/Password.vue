<script lang="ts">
import {
  ref,
  defineComponent,
} from 'vue';

import Section from '@/components/account/settings/Section.vue';
import OverlayPanel from '@/components/ui/panel/OverlayPanel.vue';
import AsyncButton from '@/components/ui/button/AsyncButton.vue';

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
    AsyncButton,
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
    <div>FOO?</div>
    <AsyncButton
      class="button"
    >
      Speichern
    </AsyncButton>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";

.button {
  @include button.default(3rem);
  min-width: 33%;
}
</style>

<script lang="ts">
import { defineComponent, ref, onActivated } from "vue";
import { useI18n } from "vue-i18n";
import { getNewsletters, updateSubscriptions } from "@/api/newsletter";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import Section from "./Section.vue";
import AsyncButton from "@/components/ui/button/AsyncButton.vue";

export default defineComponent({
  components: {
    Section,
    OverlayPanel,
    AsyncButton,
  },
  setup() {
    const { t } = useI18n();
    const newsletters = ref([]);
    const subscriptions = ref([]);
    const formVisible = ref(false);
    const showForm = () => (formVisible.value = true);
    const hideForm = async () => (formVisible.value = false);
    const loadNewsletters = async () => {
      newsletters.value = await getNewsletters();
      subscriptions.value = newsletters.value.filter((n) => n.isSubscribed).map((n) => n.uid);
    };
    const submitForm = async () => {
      await updateSubscriptions(subscriptions.value);
      await loadNewsletters();
      await hideForm();
    };
    onActivated(loadNewsletters);
    return {
      t,
      newsletters,
      subscriptions,
      formVisible,
      showForm,
      hideForm,
      submitForm,
    };
  },
});
</script>

<template>
  <Section :title="t('account.settings.newsletter.title')" @edit="showForm">
    <div v-for="newsletter in newsletters" :key="newsletter.uid" class="newsletter">
      <div>
        <span v-if="newsletter.isSubscribed">&#9679;</span>
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
    <form class="form" @submit.prevent="submitForm">
      <div class="input-container subscriptions">
        <label
          v-for="newsletter in newsletters"
          :key="`${newsletter.uid}-input`"
          class="subscription"
        >
          <input
            class="input"
            type="checkbox"
            name="subscriptions"
            :value="newsletter.uid"
            v-model="subscriptions"
          />
          <span class="title" v-text="newsletter.title" />
          <span class="description" v-text="newsletter.description" />
        </label>
      </div>
      <div class="input-container submit">
        <AsyncButton class="button" @click.prevent="submitForm" v-text="t('formActions.save')" />
      </div>
    </form>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/form";
.newsletter {
  display: flex;
  gap: 1rem;
}
.form {
  @include form.default;
  .subscriptions {
    display: flex;
    flex-direction: column;
    .subscription {
      display: grid;
      grid-template-areas:
        "checkbox title"
        "checkbox description";
      grid-template-columns: 36px 1fr;
      grid-column-gap: 1rem;
      margin-bottom: 1rem;
      > input {
        grid-area: checkbox;
        width: 36px;
        height: 36px;
      }
      > .title {
        grid-area: title;
        @include typo.large;
      }
      > .description {
        grid-area: description;
        @include typo.dim;
      }
    }
  }
}
</style>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { APIClient } from "@/api/client";
import RadioInput from "@/components/ui/form/RadioInput.vue";
import TextareaInput from "@/components/ui/form/TextareaInput.vue";
import { useAPIBaseUrl } from "@/composables/api";
import { useNotification } from "@/composables/notification";

const { t } = useI18n();
const { APIBaseUrl } = useAPIBaseUrl();
const { notify } = useNotification();

const emit = defineEmits(["close"]);

const isInterested = ref("yes");

const newsSources = ref([
  {
    value: "srf",
    title: "SRF",
    description: "Schweizer Radio und Fernsehen",
    selected: false,
  },
  {
    value: "france-info",
    title: "France Info",
    description: "",
    selected: false,
  },
  {
    value: "dlf",
    title: "DLF",
    description: "Deutschlandfunk",
    selected: false,
  },
  {
    value: "bbc",
    title: "BBC",
    description: "British Broadcasting Corporation",
    selected: false,
  },
]);

const comment = ref("");

const loadSurvey = async () => {
  const url = `${APIBaseUrl.value}survey/news/`;
  const response = await APIClient.get(url);
  return response.data;
};

const setSurvey = async (survey: any) => {
  isInterested.value = survey.isInterested ? "yes" : "no";
  comment.value = survey.comment;
  const selectedSources = survey.newsSources || [];
  selectedSources.forEach((newsSource: string) => {
    const source = newsSources.value.find((s) => s.value === newsSource);
    if (source) {
      source.selected = true;
    }
  });
};

const submitSurvey = async () => {
  const payload = {
    isInterested: isInterested.value === "yes",
    comment: "",
    newsSources: [],
  };
  if (payload.isInterested) {
    payload.comment = comment.value;
    // @ts-ignore
    payload.newsSources = newsSources.value.filter((s) => s.selected).map((s) => s.value) || [];
  }
  const url = `${APIBaseUrl.value}survey/news/`;
  const response = await APIClient.post(url, payload);
  await setSurvey(response.data);

  emit("close");

  await notify({
    level: "success",
    body: t("thankYou"),
    ttl: 5,
  });
};

onMounted(async () => {
  const survey = await loadSurvey();
  if (survey) {
    await setSurvey(survey);
  }
});
</script>

<i18n lang="yaml">
de:
  lead: "Tagesaktuelle News"
  line1: "Liebe Radiohörerin, lieber Radiohörer"
  line2: "Wir möchten gerne deine Meinung einholen, um unser Radioprogramm zu verbessern. Wir überlegen, eine neue Funktion einzuführen – eine Option, mit der du tägliche Nachrichten abrufen kannst. Mit diesem Tool kannst du Nachrichten nach Belieben aktivieren oder deaktivieren."
  line3: "Bitte nimm dir einen Moment Zeit, um uns mitzuteilen, ob du Interesse an einer solchen Funktion hast und welche Nachrichtenquellen du bevorzugst."
  interested:
    yes: "Ja, ich bin interessiert"
    no: "Nein, ich bin nicht interessiert"
  newsSources: "Nachrichtenquellen"
  comment: "Kommentar"
  submit: "Senden"
  thankYou: "Vielen Dank für dein Feedback!"
en:
  lead: "Daily News"
  line1: "Dear Radio Listener,"
  line2: "We're seeking your input to enhance our radio programming. We're considering introducing a new feature – an option that allows you to access daily news updates. This would enable you to stay informed about current events quickly and easily. With this tool, you can activate or deactivate news as per your preference effortlessly."
  line3: "Please take a moment to let us know if you're interested in such a feature and which news sources you prefer."
  interested:
    yes: "Yes, I'm interested"
    no: "No, I'm not interested"
  newsSources: "News Sources"
  comment: "Comment"
  submit: "Submit"
  thankYou: "Thanks a lot for your feedback!"
</i18n>

<template>
  <form class="prompt">
    <div class="prompt__lead">
      <p v-text="t('lead')" />
    </div>
    <div class="prompt__intro">
      <p v-text="t('line1')" />
      <p v-text="t('line2')" />
      <p v-text="t('line3')" />
    </div>
    <div class="prompt__interest">
      <RadioInput v-model="isInterested" :label="t('interested.yes')" value="yes" name="interest" />
      <RadioInput v-model="isInterested" :label="t('interested.no')" value="no" name="interest" />
    </div>
    <div v-if="isInterested == 'yes'">
      <div class="prompt__sources">
        <div class="source-title">
          <span v-text="t('newsSources')" />
        </div>
        <div class="source-options">
          <label v-for="s in newsSources" :key="`source-${s.value}`" class="option">
            <input class="input" type="checkbox" v-model="s.selected" />
            <span class="title">{{ s.title }}</span>
            <span class="description">{{ s.description }}</span>
          </label>
        </div>
      </div>
      <div class="prompt__comment">
        <TextareaInput v-model="comment" :maxlength="256" :label="t('comment')" />
      </div>
    </div>
    <div class="prompt__actions">
      <button class="button" @click.prevent="submitSurvey" v-text="t('submit')" />
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/form";
@use "@/style/elements/button";

.prompt {
  margin-bottom: calc(72px + 1rem); /* player height + margin */

  @include form.default;

  &__lead {
    padding: 0 0 1rem;

    @include typo.large;
  }

  &__intro {
    padding: 0 0 1rem;

    @include typo.default;

    > p {
      margin-bottom: 1rem;
    }
  }

  &__interest {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  &__sources {
    padding: 2rem 0 1rem;

    .source-title {
      margin-bottom: 1rem;
    }

    .source-options {
      display: grid;

      @include responsive.bp-medium-up {
        grid-template-columns: 1fr 1fr;
      }

      > .option {
        display: grid;
        grid-template-areas:
          "checkbox title"
          "checkbox description";
        grid-template-columns: 36px 1fr;
        grid-column-gap: 1rem;
        margin-bottom: 1rem;

        > input {
          height: 36px;
          width: 36px;
          grid-area: checkbox;
          align-self: start;
          margin-top: 4px;
        }

        > .title {
          grid-area: title;

          @include typo.default;
        }

        > .description {
          grid-area: description;

          @include typo.dim;
        }
      }
    }
  }

  &__comment {
    padding: 1rem 0 0;

    textarea {
      @include typo.large;

      width: 100%;
      min-height: 4rem;
      padding: 0.54rem;
    }
  }

  &__actions {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 2rem 0 1rem;

    .button {
      @include button.default(3rem);

      min-width: 33%;
    }
  }
}
</style>

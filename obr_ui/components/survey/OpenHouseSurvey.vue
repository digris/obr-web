<script setup lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const emit = defineEmits(["close"]);

const SURVEY_URL = "https://forms.gle/EhoPVLJnVL3uBHBV9";

const openSurvey = async () => {
  window.open(SURVEY_URL, "_blank");
  emit("close");
};
</script>

<i18n lang="yaml">
de:
  lead: "Open Broadcast öffnet seine Türen"
  lead2: "Samstag, 27. Juni, ab 16 Uhr"
  line1: "Komm vorbei und wirf einen Blick hinter die Kulissen von Open Broadcast."
  line2: "Wir erzählen, wie unsere Radioidee entstand, wie Open Broadcast das Radioangebot in der Schweiz verdoppelte – und warum Radio bis heute neugierig bleibt."
  line3: "Es gibt Essen, Getränke, Musik und Spielmöglichkeiten für Kinder."
  line4: |
    Open Broadcast Radio
    Lessingstrasse 33, 8002 Zürich
      Ab 16 Uhr bis open end
  greeting: "Stay curious!"
  participate: "Anmelden"

en:
  lead: "Open Broadcast opens its doors"
  lead2: "Saturday, June 27, from 4 PM"
  line1: "Come by and take a look behind the scenes at Open Broadcast."
  line2: "We’ll share how our radio idea began, how Open Broadcast doubled the radio offering in Switzerland — and why radio remains curious to this day."
  line3: "There will be food, drinks, music and activities for children."
  line4: |
    Open Broadcast Radio
    Lessingstrasse 33, 8002 Zurich
    From 4 PM until late
  greeting: "Stay curious!"
  participate: "Register"
</i18n>

<template>
  <form class="prompt">
    <div class="prompt__lead">
      <p v-text="t('lead')" />
      <p v-text="t('lead2')" />
    </div>
    <div class="prompt__intro">
      <p v-text="t('line1')" />
      <p v-text="t('line2')" />
      <p v-text="t('line3')" />
      <p v-text="t('line4')" class="address" />
      <p v-text="t('greeting')" class="greeting" />
    </div>
    <div class="prompt__actions">
      <button class="button" @click.prevent="openSurvey" v-text="t('participate')" />
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/button";

.prompt {
  margin-bottom: calc(72px + 1rem); /* player height + margin */

  &__lead {
    padding: 0 0 1rem;

    @include typo.large;
  }

  &__intro {
    padding: 0 0 1rem;

    @include typo.default;

    > p {
      margin-bottom: 1rem;

      &.address {
        white-space: pre-line;
      }

      &.greeting {
        margin-top: 2rem;
      }
    }

    > h4 {
      margin-bottom: 0.25rem;

      @include typo.bold;
    }
  }

  &__actions {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 2rem;
    padding: 1rem 0;

    .button {
      @include button.default(3rem);

      min-width: 33%;
    }
  }
}
</style>

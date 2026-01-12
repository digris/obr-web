<script setup lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const emit = defineEmits(["close"]);

const SURVEY_URL = "https://surveyc.sotomo.info/index.php?r=survey/index&sid=755183";

const openSurvey = async () => {
  window.open(SURVEY_URL, "_blank");
  emit("close");
};
</script>

<i18n lang="yaml">
de:
  lead: "Hilf mit, neue und spezialisierte Radios sichtbar zu machen"
  line1: "Liebe Radiohörerin, lieber Radiohörer"
  line2: "Diese Umfrage wird vom Forschungsinstitut Sotomo durchgeführt. Sie ist Teil der neuen Reichweitenmessung radio-data.ch, welche dieses Jahr das erste Mal veröffentlicht wird."
  line3: "Warum ist das wichtig?"
  line4: "Die aktuelle Messlogik ist primär auf grosse, etablierte Programme ausgelegt und eignet sich nur bedingt für digitale, neue oder spezialisierte Radioprogramme. Dadurch entsteht eine methodisch bedingte Untererfassung, die weniger über die tatsächliche Nutzung als über die Grenzen der Messmethode aussagt. Die neue digitale Messmethode schliesst diese Lücke und macht auch spezialisierte Radios erstmals sichtbar für die Forschung, Werbung, Politik, Behörden und Kulturförderung."
  line5: "Die Umfrage dauert nur 5–10 Minuten, ist anonym und bildet auch eine wichtige Grundlage für die medienpolitische Anerkennung. Je mehr Menschen teilnehmen, desto belastbarer und aussagekräftiger sind die Ergebnisse."
  participate: "Teilnehmen"
en:
  lead: "Help make new and specialised radio stations visible"
  line1: "Dear radio listener"
  line2: "This survey is conducted by the research institute Sotomo. It is part of the new audience measurement radio-data.ch, which will be published for the first time this year."
  line3: "Why is this important?"
  line4: "The current measurement logic is primarily designed for large, established programmes and is only partially suitable for digital, new or specialised radio stations. This leads to a methodologically driven underrepresentation that says less about actual usage than about the limitations of the measurement method. The new digital measurement approach closes this gap and, for the first time, makes specialised radio stations visible to research, advertising, politics, public authorities and cultural funding bodies."
  line5: "The survey takes only 5–10 minutes, is anonymous, and also provides an important basis for media policy recognition. The more people participate, the more robust and meaningful the results will be."
  participate: "Participate"
</i18n>

<template>
  <form class="prompt">
    <div class="prompt__lead">
      <p v-text="t('lead')" />
    </div>
    <div class="prompt__intro">
      <p v-text="t('line1')" />
      <p v-text="t('line2')" />
      <h4 v-text="t('line3')" />
      <p v-text="t('line4')" />
      <p v-text="t('line5')" />
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

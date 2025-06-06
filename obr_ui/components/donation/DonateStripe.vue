<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
const isStripeReady = ref(false);

onMounted(() => {
  if (customElements.get("stripe-buy-button")) {
    isStripeReady.value = true;
    return;
  }

  const script = document.createElement("script");
  script.src = "https://js.stripe.com/v3/buy-button.js";
  script.async = true;
  script.onload = () => {
    if (customElements.get("stripe-buy-button")) {
      isStripeReady.value = true;
    }
  };
  document.head.appendChild(script);
});
</script>

<i18n lang="yaml">
de:
  lead: "Tagesaktuelle News"
  line1: "Liebe Radiohörerin, lieber Radiohörer"
  line2: "Wir möchten gerne deine Meinung einholen, um unser Radioprogramm zu verbessern. Wir überlegen, eine neue Funktion einzuführen – eine Option, mit der du tägliche Nachrichten abrufen kannst. Mit diesem Tool kannst du Nachrichten nach Belieben aktivieren oder deaktivieren."
  line3: "Bitte nimm dir einen Moment Zeit, um uns mitzuteilen, ob du Interesse an einer solchen Funktion hast und welche Nachrichtenquellen du bevorzugst."
en:
  lead: "Daily News"
  line1: "Dear Radio Listener,"
  line2: "We're seeking your input to enhance our radio programming. We're considering introducing a new feature – an option that allows you to access daily news updates. This would enable you to stay informed about current events quickly and easily. With this tool, you can activate or deactivate news as per your preference effortlessly."
  line3: "Please take a moment to let us know if you're interested in such a feature and which news sources you prefer."
</i18n>

<template>
  <div class="prompt">
    <div class="prompt__lead">
      <p v-text="t('lead')" />
    </div>
    <div class="prompt__intro">
      <p v-text="t('line1')" />
      <p v-text="t('line2')" />
      <p v-text="t('line3')" />
    </div>
    <div v-if="isStripeReady" class="prompt__actions">
      <stripe-buy-button
        buy-button-id="buy_btn_1QmsRaE8KzeSVu8lq4qLbQAF"
        publishable-key="pk_test_51Oo27aE8KzeSVu8lSnFuT4hJGQTJNW4tC4BXTSii61fVvGCoWSHjNAJEkNB9oMlb27xJOmdIxKFMd2l5Llmq4Ubc00McFuC8yp"
      />
    </div>
  </div>
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

  &__actions {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    padding: 2rem 0 1rem;

    .button {
      @include button.default(3rem);

      min-width: 33%;
    }
  }
}
</style>

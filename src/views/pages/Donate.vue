<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import twintQrCode from "@/assets/pages/donate/twint-qr-code.png";
import Page from "@/views/pages/Page.vue";

export default defineComponent({
  components: {
    Page,
  },
  setup() {
    const { t } = useI18n();
    return {
      t,
      twintQrCode,
    };
  },
});
</script>

<i18n lang="yaml">
de:
  title: Spenden
  lead: Du kannst uns gerne mit einer Spende unterstützen.
  bankTransfer: Überweisung
  thankYou: Wir danken für die Unterstützung!
en:
  title: Donate
  lead: Support us
  bankTransfer: Wire
  thankYou: THX
</i18n>

<template>
  <Page :title="t('title')">
    <template #lead>
      {{ t("lead") }}
    </template>
    <div class="donate">
      <div class="method transfer">
        <h3 v-text="t('bankTransfer')" />
        <p>
          IBAN: CH68 0900 0000 8537 9408 6<br />
          PC: 85-379408-6<br />
          BIC: POFICHBEXXX
        </p>
      </div>
      <div class="method twint">
        <h3>Twint</h3>
        <a href="https://pay.raisenow.io/kytbj" target="_blank">
          <img class="logo" :src="twintQrCode" />
        </a>
      </div>
    </div>
    <!--
    <div class="note">
      <p v-text="t('thankYou')" />
    </div>
    -->
    <i18n-t keypath="thankYou" class="note" />
  </Page>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";

.donate {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: 1fr 1fr;

  .method {
    h3 {
      margin-bottom: 1rem;
    }

    &.twint {
      img {
        max-width: 50%;
      }
    }
  }
  @include responsive.bp-medium {
    grid-template-columns: unset;

    .method {
      margin-bottom: 2rem;

      &.twint {
        > a {
          display: flex;
          justify-content: center;
        }

        img {
          max-width: 75%;
        }
      }
    }
  }
}

.note {
  margin-top: 1rem;
}
</style>

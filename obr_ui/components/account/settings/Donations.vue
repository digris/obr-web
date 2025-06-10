<script lang="ts" setup>
import { computed, defineProps } from "vue";
import { useI18n } from "vue-i18n";

import Datetime from "@/components/ui/date/Datetime.vue";
import eventBus from "@/eventBus";

import Section from "./Section.vue";

const STRIPE_SELF_SERVICE_PORTAL_URL =
  "https://billing.stripe.com/p/login/test_6oU28re1Mbb42gU6KA2oE00";

const props = defineProps<{
  donations?: any[];
}>();

const { t } = useI18n();

const recurringDonations = computed(() => {
  return props.donations?.filter((d) => d.kind === "recurring" && d.state === "active") || [];
});

const singleDonations = computed(() => {
  return props.donations?.filter((d) => d.kind === "single" && d.state === "succeeded") || [];
});

const createDonation = () => {
  eventBus.emit("donation:showPanel");
};

const cancelDonation = (uid: string) => {
  console.debug("cancelDonation", uid);
  // NOTE: for the moment we just open the stripe self-service portal
  window.open(STRIPE_SELF_SERVICE_PORTAL_URL, "_blank");
};
</script>

<template>
  <Section :title="t('account.settings.donations.title')" :outlined="false">
    <!--
    <pre v-text="donations" />
    -->
    <div class="info">
      <i18n-t keypath="account.settings.donations.info" tag="p" />
    </div>
    <div v-if="!recurringDonations.length" class="create-donation">
      <div>
        <button @click.prevent="createDonation()">Spende einrichten</button>
      </div>
    </div>
    <div v-if="recurringDonations.length" class="donations donations--recurring">
      <p class="info">Wiederkehrende Spenden</p>
      <div
        v-for="donation in recurringDonations"
        :key="`recurring-donation-${donation.uid}`"
        class="donation donation--recurring"
      >
        <div class="amount">
          <span v-text="donation.currency" />
          <span
            v-text="
              parseFloat(donation.amount).toLocaleString('de-CH', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })
            "
          />
        </div>
        <div class="created">
          <!--
          <Datetime :value="donation.created" />
          -->
        </div>
        <div class="state">{{ donation.state }}</div>
        <div class="actions">
          <button @click.prevent="cancelDonation(donation.uid)" class="button button--cancel">
            Beenden
          </button>
        </div>
      </div>
    </div>
    <div v-if="singleDonations.length" class="donations donations--single">
      <p class="info">Einmalige Spenden</p>
      <div
        v-for="donation in singleDonations"
        :key="`single-donation-${donation.uid}`"
        class="donation donation--single"
        :class="`donation--${donation.state}`"
      >
        <div class="amount">
          <span v-text="donation.currency" />
          <span
            v-text="
              parseFloat(donation.amount).toLocaleString('de-CH', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })
            "
          />
        </div>
        <div class="created">
          <Datetime :value="donation.created" />
        </div>
        <div class="state">{{ donation.state }}</div>
        <div />
      </div>
    </div>
  </Section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/button";

.info {
  padding: 0 2rem 1rem 0;
  opacity: 0.5;
  white-space: pre-line;

  @include responsive.bp-medium {
    @include typo.small;
  }
}

.create-donation {
  margin-top: 1rem;
  display: flex;
  justify-content: center;

  button {
    @include button.outlined(2.5rem);

    min-width: 33%;
  }
}

.donations {
  margin-top: 1rem;

  .donation {
    display: grid;
    grid-template-columns: 120px auto 100px 120px;
    grid-gap: 0.25rem;
    align-items: center;
    margin-bottom: 0.5rem;
    padding: 0.25rem 0.25rem 0.25rem 1rem;
    color: rgb(var(--c-dark));

    &--recurring {
      border: 1px solid rgb(var(--c-dark) / 20%);
      border-radius: 3px;
    }

    &--single {
      background: rgb(var(--c-dark) / 2.5%);
      border-radius: 3px;
    }

    &--succeeded {
      background: rgb(var(--c-green) / 10%);
      border-radius: 3px;
    }

    > .amount {
      display: flex;
      gap: 0.25rem;
    }

    > .created {
      @include typo.light;
    }

    > .state {
      @include typo.tiny;
      @include typo.light;

      text-transform: uppercase;
    }

    > .actions {
      .button {
        @include typo.tiny;

        min-width: 120px;
        padding: 0.75rem 1.5rem;
        background: rgb(var(--c-dark) / 10%);
        border: 0;
        cursor: pointer;
        color: rgb(var(--c-dark));
        text-transform: uppercase;

        [data-theme="dark"] & {
          background: rgb(var(--c-dark) / 10%);
        }

        &--cancel {
          background: rgb(var(--c-red) / 10%);
          color: rgb(var(--c-red));

          &:hover {
            background: rgb(var(--c-red) / 15%);
          }
        }
      }
    }
  }
}
</style>

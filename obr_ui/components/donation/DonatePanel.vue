<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";

import IconClose from "@/components/ui/icon/IconClose.vue";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

import FlowRecurring from "./flow/FlowRecurring.vue";
import FlowSingle from "./flow/FlowSingle.vue";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const { loadUser, user } = useAccount();

const hasActiveDonation = ref(false);

const updateActiveDonation = () => {
  /* @ts-ignore */
  hasActiveDonation.value = !!(user.value?.donations ?? []).find((d) => d.state === "active");
};

onMounted(() => {
  // NOTE: we only run this on mounted, so the panel does not change
  //       when the user creates a new recurring donation ;)
  updateActiveDonation();
});

watch(
  () => route.hash,
  (newHash) => {
    if (!newHash.startsWith("#donate:")) {
      return;
    }
    const kind = newHash.replace("#donate:", "");
    if (["single", "recurring"].includes(kind)) {
      isVisible.value = true;
      setKind(kind);
      setStep("amount");
      router.replace({ hash: "" });
    }
    if (["success"].includes(kind)) {
      isVisible.value = true;
      setStep("success");
      router.replace({ hash: "" });
    }
  }
);

const isVisible = ref(false);
const kind = ref("single");

const step = ref("amount"); // amount / payment / success
const successData = ref<object | null>(null); // data from the payment step

const currencies = ["CHF", "EUR", "USD"];
const currency = ref("CHF");

const setKind = (value: string) => {
  kind.value = value;
};

const close = () => {
  isVisible.value = false;
  setStep("amount");
};

const infoVisible = computed(() => {
  return ["amount"].includes(step.value);
});

const navVisible = computed(() => {
  return ["amount"].includes(step.value);
});

const flowVisible = computed(() => {
  return step.value !== "success";
});

const successVisible = computed(() => {
  return step.value === "success";
});

eventBus.on("donation:showPanel", () => {
  updateActiveDonation();
  isVisible.value = true;
});

eventBus.on("donation:hidePanel", () => {
  isVisible.value = false;
});

eventBus.on("donation:togglePanel", () => {
  updateActiveDonation();
  isVisible.value = !isVisible.value;
});

const setStep = (value: string) => {
  step.value = value;
  console.debug("DonatePanel:setStep", value);
};

const onStep = (value: string) => {
  console.debug("DonatePanel:onStep", value);
  setStep(value);
};

const onSuccess = (response: object) => {
  console.debug("DonatePanel:onSuccess", response);
  successData.value = response;
  loadUser(); // make sure the donation status is updated
  setStep("success");
};
</script>

<template>
  <transition name="fade">
    <div v-if="false" @click="close" class="mask" />
  </transition>
  <transition name="slide">
    <div v-if="isVisible" class="panel">
      <div class="close">
        <IconClose @click.prevent="close" :style="{ '--c-fg': 'var(--c-white)' }" />
      </div>
      <!--
      <pre v-text="{infoVisible, navVisible, kind, step}" />
      -->
      <div v-if="hasActiveDonation" class="body">
        <div class="info">
          <h2>Vielen Dank!</h2>
          <p>Du hast bereits eine wiederkehrende Spende eingerichtet.</p>
          <p>
            Wenn du deine regelmässige Spende ändern oder canceln möchtest findest du alles nötige
            in deinm Konto
          </p>
        </div>
        <div class="actions">
          <router-link
            :to="{ name: 'accountSettings' }"
            class="action action--continue"
            v-text="t('menu.accountSettings')"
          />
        </div>
      </div>
      <div v-else class="body">
        <div v-if="infoVisible" class="info">
          <h2>Support Our Work</h2>
          <p>Your contributions help us keep the project alive!</p>
        </div>
        <div v-if="navVisible" class="nav">
          <div class="currency">
            <select v-model="currency">
              <option v-for="c in currencies" :key="`option-currency-${c}`" :value="c">
                {{ c }}
              </option>
            </select>
          </div>
          <div class="kinds">
            <div
              @click.prevent="setKind('single')"
              class="kind kind--single"
              :class="{
                'is-selected': kind === 'single',
              }"
            >
              Einmalig
            </div>
            <div
              @click.prevent="setKind('recurring')"
              class="kind kind--recurring"
              :class="{
                'is-selected': kind === 'recurring',
              }"
            >
              Monatlich
            </div>
          </div>
          <div class="alt">
            <div></div>
          </div>
        </div>
        <div v-if="flowVisible" class="flow">
          <div v-if="kind === 'single'">
            <FlowSingle @step="onStep" @success="onSuccess" :currency="currency" />
          </div>
          <div v-if="kind === 'recurring'">
            <FlowRecurring @step="onStep" @success="onSuccess" :currency="currency" />
          </div>
        </div>
        <div v-if="successVisible" class="success">
          <h2>Vielen Dank!</h2>
          <p>
            Deine Spende hilft uns, ein unabhängiges und vielseitiges Radioprogramm am Leben zu
            erhalten.
          </p>
          <p>❤️❤️❤️❤️❤️❤️</p>
          <p>
            Mit deinem Beitrag ermöglichst du die fortlaufende, sorgfältige Musik-Kuration jenseits
            des Mainstreams – handverlesen, überraschend und unkommerziell.
          </p>
          <!--
          <div v-if="successData && successData?.invoice">
            <a :href="successData.invoice.pdfInvoiceUrl">Invoice (PDF)</a>
          </div>
          -->
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/button";

@keyframes steam {
  0% {
    background-position: 0 0;
  }

  50% {
    background-position: 400% 0;
  }

  100% {
    background-position: 0 0;
  }
}

.mask {
  top: 0;
  position: fixed;
  height: 100%;
  width: 100%;
  z-index: 20;
  left: 0;

  /*
  background: rgb(var(--c-black) / 50%);
  */

  /*
  @include responsive.bp-medium {
    background: unset;
  }
  */
}

.panel {
  z-index: 20;
  position: fixed;
  width: 100%;
  max-width: min(460px, calc(100vw - 2rem));
  bottom: 5.5rem;
  padding: 0;
  right: 1rem;
  border-radius: 1rem;

  /* overflow-y: auto; */

  color: rgb(var(--c-white));
  background: rgb(var(--c-black));
  overscroll-behavior: contain;

  /*
  &::before,
  &::after {
    opacity: 0.1;
    top: -2px;
    position: absolute;
    height: calc(100% + 4px);
    width: calc(100% + 4px);
    content: "";
    left: -2px;
    background: linear-gradient(45deg, #f0f, #0ff, #f0f);
    background-size: 400%;
    z-index: -1;
    animation: steam 20s linear infinite;
    border-radius: 1rem;
  }

  &::after {
    filter: blur(10px);
  }
  */

  @include responsive.bp-medium {
    background: rgb(var(--c-black));
    max-width: 100vw;
    right: unset;
    border-radius: 1rem 1rem 0 0;
    bottom: 0;
    padding-bottom: 5.5rem;
    z-index: 100; // move above legal-disclaimer
  }

  > .close {
    top: 4px;
    position: absolute;
    right: 4px;
    cursor: pointer;
  }

  > .body {
    padding: 1rem;

    > .info {
      color: currentcolor;

      > h2 {
        margin-bottom: 0.5rem;
      }

      > p {
        &:not(:last-child) {
          margin-bottom: 0.5rem;
        }
      }
    }

    > .actions {
      margin-top: 2rem;

      > .action {
        @include button.default;

        color: rgba(var(--c-white) / 100%);
        width: 100%;
        background: rgb(var(--c-green) / 100%);

        &:not(:disabled) {
          @include responsive.on-hover {
            background: rgb(var(--c-green) / 90%);
          }
        }
      }
    }

    > .nav {
      margin-top: 2rem;
      margin-bottom: 2rem;
      display: grid;
      grid-template-columns: 100px 1fr 100px;

      > .currency {
        display: flex;
        align-items: center;
        justify-content: flex-start;

        > select {
          @include typo.default;
          @include typo.bold;

          position: relative;
          outline: none;
          background: rgb(var(--c-black) / 50%);
          border: none;
          color: rgb(var(--c-white));
        }
      }

      > .kinds {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;

        > .kind {
          cursor: pointer;
          padding: 0.25rem 0.5rem;
          border-bottom: 2px solid rgb(var(--c-green) / 0%);

          &.is-selected {
            color: rgb(var(--c-white));
            border-bottom: 2px solid rgb(var(--c-green) / 100%);
          }
        }
      }

      > .alt {
        display: flex;
        align-items: center;
        justify-content: flex-end;
      }
    }

    > .flow {
      color: currentcolor;
    }

    > .success {
      padding-bottom: 4rem;

      > h2 {
        margin-bottom: 0.5rem;
      }

      /* stylelint-disable-next-line no-descending-specificity */
      > p {
        max-width: 90%;

        &:not(:last-child) {
          margin-bottom: 0.5rem;
        }
      }
    }
  }
}
</style>

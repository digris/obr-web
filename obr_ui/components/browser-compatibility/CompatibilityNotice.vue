<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useStorage } from "@vueuse/core";

import ModalPanel from "@/components/ui/panel/ModalPanel.vue";
import { useDevice } from "@/composables/device";

const FAQ_LINK = "/faq/#007FC4FA";

const BROWSER_REQUIREMENTS = {
  macos: {
    safari: ">=15",
  },

  desktop: {
    chrome: ">=100",
    firefox: ">=100",
    opera: ">=80",
  },

  mobile: {
    safari: ">=15",
  },

  ios: {
    safari: ">=15",
  },
};

const { t } = useI18n();
const router = useRouter();
const { uaParser, isApp } = useDevice();

// const os = uaParser.getOS();
const browser = uaParser.getBrowser();
const platform = uaParser.getPlatform();
const engine = uaParser.getEngine();

const isVisible = ref(false);
const isDismissed = useStorage("browser-compatibility/notice/dismissed", false);
const browserDisplay = ref("");

const close = () => {
  isDismissed.value = true;
  isVisible.value = false;
};

const navigateToFaq = () => {
  close();
  router.push(FAQ_LINK);
};

onMounted(() => {
  if (isApp || isDismissed.value) {
    return;
  }
  const isSupportedBrowser = uaParser.satisfies(BROWSER_REQUIREMENTS);
  if (!isSupportedBrowser) {
    browserDisplay.value = `${browser.name} ${browser.version}`;
    isVisible.value = true;
  }
});
</script>

<template>
  <ModalPanel :is-visible="isVisible" title="Browser Support" @close="close">
    <div class="not-supported">
      <i18n-t keypath="browserCompatibility.notSupported.note" tag="p" class="note">
        {{ browserDisplay }}
      </i18n-t>
      <i18n-t keypath="browserCompatibility.notSupported.faqNote" tag="p" class="faq-note">
        <a
          href="#"
          @click.prevent="navigateToFaq"
          v-text="t('browserCompatibility.notSupported.faqLabel')"
        />
      </i18n-t>
    </div>
    <pre
      v-if="false"
      v-text="{
        browser,
        engine,
        platform,
      }"
    />
    <!--
    <template #footer>
      <p>Detected browser: <span v-text="browserDisplay" /></p>
    </template>
    -->
  </ModalPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/section";

.not-supported {
  margin-bottom: 2rem;
}

.faq-note {
  margin-top: 1rem;

  a {
    text-decoration: underline;
    cursor: pointer;
  }
}

.legal {
  font-size: 90%;
  opacity: 0.5;
}
</style>

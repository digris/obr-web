<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

import LanguageChooser from "@/components/navigation/LanguageChooser.vue";
import ToggleDarkModeButton from "@/components/navigation/ToggleDarkModeButton.vue";
import SidePanel from "@/components/ui/panel/SidePanel.vue";
import { useAccount } from "@/composables/account";
import { useDevice } from "@/composables/device";
import { useSubscription } from "@/composables/subscription";
import eventBus from "@/eventBus";

export default defineComponent({
  components: {
    SidePanel,
    LanguageChooser,
    ToggleDarkModeButton,
  },
  setup() {
    const router = useRouter();
    const { t } = useI18n();
    const isVisible = ref(false);
    const { user, isStaff, logoutUser } = useAccount();
    const { isApp } = useDevice();
    const { userVouchers } = useSubscription();
    const close = () => {
      isVisible.value = false;
    };
    eventBus.on("side-menu:show", () => {
      isVisible.value = true;
    });
    const login = () => {
      const event = {
        intent: "login",
        next: window.location.pathname,
      };
      eventBus.emit("account:authenticate", event);
    };
    const logout = async () => {
      try {
        await logoutUser();
        await router.push({ name: "home" });
        close();
      } catch (err) {
        console.debug("err", err);
      }
    };
    const pages = computed(() => {
      return [
        {
          path: "/faq/",
          title: t("menu.faq"),
        },
        {
          path: "/about/",
          title: t("menu.about"),
        },
        {
          path: "/contact/",
          title: t("menu.contact"),
        },
        {
          path: "/donate/",
          title: t("menu.donate"),
        },
        {
          path: "/developers/",
          title: t("menu.developers"),
        },
        {
          path: "/legal/imprint/",
          title: t("menu.imprint"),
        },
        {
          path: "/legal/terms/",
          title: t("menu.terms"),
        },
      ];
    });
    const onNavigate = () => {
      close();
    };
    return {
      t,
      close,
      onNavigate,
      isVisible,
      user,
      isStaff,
      userVouchers,
      login,
      logout,
      pages,
      isApp,
    };
  },
});
</script>
<template>
  <SidePanel :is-visible="isVisible" @close="close">
    <div class="side-menu">
      <section class="section" v-if="user">
        <router-link
          :to="{
            name: 'accountSettings',
          }"
          @click="onNavigate"
          v-text="t('menu.accountSettings')"
        />
        <a v-if="isStaff" href="/admin/" target="_blank" v-text="t('menu.admin')" />
        <!---->
        <router-link
          v-if="userVouchers.length"
          :to="{
            name: 'accountUserVouchers',
          }"
          @click="onNavigate"
          v-text="t('menu.userVouchers')"
        />
      </section>
      <section class="section" v-else>
        <a href="#" @click.prevent="login"> Login </a>
      </section>
      <section class="section section--primary">
        <router-link
          :to="{
            name: 'home',
          }"
          @click="onNavigate"
          v-text="t('menu.home')"
        />
        <router-link
          :to="{
            name: 'discover',
          }"
          @click="onNavigate"
          v-text="t('menu.discover')"
        />
        <router-link
          :to="{
            name: 'collection',
          }"
          @click="onNavigate"
          v-text="t('menu.collection')"
        />
      </section>
      <section class="section section--primary">
        <router-link
          :to="{
            name: 'programRedirect',
          }"
          @click="onNavigate"
          v-text="t('menu.program')"
        />
        <router-link
          :to="{
            path: '/reception/',
          }"
          @click="onNavigate"
          v-text="t('menu.reception')"
        />
      </section>
      <section class="section">
        <router-link v-if="isApp" :to="{ name: 'protoAppBridge' }">APP</router-link>
        <router-link
          v-for="(page, index) in pages"
          :key="`page-${index}-${page.path}`"
          :to="page.path"
          @click="onNavigate"
          v-text="page.title"
        />
      </section>
      <section class="section" v-if="user">
        <a href="#" @click.prevent="logout" v-text="t('menu.logout')" />
      </section>
    </div>
    <template #footer>
      <div class="footer">
        <div class="ui-mode-chooser">
          <ToggleDarkModeButton />
        </div>
        <LanguageChooser class="language-chooser" />
      </div>
    </template>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/section";
@use "@/style/base/typo";

.side-menu {
  overflow-y: auto;
  max-height: 100%;
  overscroll-behavior: contain;

  .section {
    display: flex;
    flex-direction: column;
    padding: 14px 0;

    &:first-child {
      padding-top: 7px;
    }

    &:not(:last-child) {
      border-bottom: 1px solid rgb(var(--c-dark) / 20%);
    }

    > a {
      line-height: 150%;

      &:hover {
        opacity: 0.5;
      }
    }

    &--primary {
      /* stylelint-disable-next-line no-descending-specificity */
      > a {
        @include typo.bold;

        font-size: 4rem;
        line-height: 100%;
      }
    }
  }
  @include responsive.bp-medium {
    .section {
      padding: 10px 0;

      &:first-child {
        padding-top: 10px;
      }

      &--primary {
        > a {
          font-size: 2.5rem;
        }

        padding: 12px 0;
      }
    }
  }
}

.footer {
  display: flex;
  min-height: 2rem;
  align-items: center;

  .ui-mode-chooser {
    flex-grow: 1;
  }
}
</style>

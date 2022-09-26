<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import eventBus from "@/eventBus";
import SidePanel from "@/components/ui/panel/SidePanel.vue";
import LanguageChooser from "@/components/navigation/LanguageChooser.vue";
import ToggleThemeButton from "@/components/navigation/ToggleThemeButton.vue";

export default defineComponent({
  components: {
    SidePanel,
    LanguageChooser,
    ToggleThemeButton,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const { t } = useI18n();
    const isVisible = ref(false);
    const user = computed(() => store.getters["account/user"]);
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
        await store.dispatch("account/logoutUser");
        await router.push({ name: "home" });
        close();
      } catch (err) {
        console.debug("err", err);
      }
    };
    const pages = computed(() => {
      return [
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
      login,
      logout,
      pages,
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
          <ToggleThemeButton />
        </div>
        <LanguageChooser class="language-chooser" />
      </div>
    </template>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/section";
@use "@/style/base/typo";
.side-menu {
  overflow-y: scroll;
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
      border-bottom: 1px solid rgb(var(--c-gray-200));
    }
    > a {
      line-height: 150%;
      &:hover {
        opacity: 0.5;
      }
    }
    &--primary {
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
  border-top: 1px solid rgb(var(--c-gray-200));
  padding-top: 0.5rem;
  padding-bottom: 1rem;
  .ui-mode-chooser {
    flex-grow: 1;
  }
}
</style>

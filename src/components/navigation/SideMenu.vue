<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import eventBus from "@/eventBus";
import SidePanel from "@/components/ui/panel/SidePanel.vue";

export default defineComponent({
  components: {
    SidePanel,
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
    const navigate = async (e: any) => {
      await router.push(e);
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
          path: "/legal/imprint/",
          title: t("menu.imprint"),
        },
        {
          path: "/legal/terms/",
          title: t("menu.terms"),
        },
      ];
    });
    return {
      t,
      close,
      isVisible,
      user,
      navigate,
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
          to="/"
          @click.prevent="
            navigate({
              name: 'accountSettings',
            })
          "
          v-text="t('menu.accountSettings')"
        />
      </section>
      <section class="section" v-else>
        <a href="#" @click.prevent="login"> Login </a>
      </section>
      <section class="section section--primary">
        <router-link
          to="/"
          @click.prevent="
            navigate({
              name: 'home',
            })
          "
          v-text="t('menu.home')"
        />
        <router-link
          to="/discover/"
          @click.prevent="
            navigate({
              name: 'discover',
            })
          "
          v-text="t('menu.discover')"
        />
        <router-link
          to="/collection/"
          @click.prevent="
            navigate({
              name: 'collection',
            })
          "
          v-text="t('menu.collection')"
        />
      </section>
      <section class="section section--primary">
        <router-link
          to="/program/"
          @click.prevent="
            navigate({
              name: 'program',
            })
          "
          v-text="t('menu.program')"
        />
        <router-link to="/reception/" v-text="t('menu.reception')" />
      </section>
      <section class="section">
        <router-link
          v-for="(page, index) in pages"
          :key="`page-${index}-${page.path}`"
          :to="page.path"
          @click.prevent="
            navigate({
              path: page.path,
            })
          "
          v-text="page.title"
        />
      </section>
      <section class="section" v-if="user">
        <a href="#" @click.prevent="logout" v-text="t('menu.logout')" />
      </section>
    </div>
  </SidePanel>
</template>

<style lang="scss" scoped>
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
    &--primary {
      > a {
        @include typo.bold;
        font-size: 4rem;
        line-height: 4rem !important;
      }
    }
    > a {
      line-height: 1.5rem;
      &:hover {
        opacity: 0.5;
      }
    }
  }
}
</style>

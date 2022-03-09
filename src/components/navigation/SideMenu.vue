<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import eventBus from '@/eventBus';
import SidePanel from '@/components/ui/panel/SidePanel.vue';

export default defineComponent({
  components: {
    SidePanel,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const isVisible = ref(false);
    const user = computed(() => store.getters['account/user']);
    const close = () => {
      isVisible.value = false;
    };
    const navigate = async (e:any) => {
      await router.push(e);
      isVisible.value = false;
    };
    eventBus.on('side-menu:show', () => {
      isVisible.value = true;
    });
    const login = () => {
      const event = {
        intent: 'login',
        next: window.location.pathname,
      };
      eventBus.emit('account:authenticate', event);
    };
    const logout = async () => {
      try {
        await store.dispatch('account/logoutUser');
        await router.push({ name: 'home' });
        close();
      } catch (err) {
        console.debug('err', err);
      }
    };
    return {
      close,
      isVisible,
      user,
      navigate,
      login,
      logout,
    };
  },
});
</script>
<template>
  <SidePanel
    :is-visible="isVisible"
    @close="close"
  >
    <div
      class="side-menu"
    >
      <section
        class="section"
        v-if="user"
      >
        <router-link
          to="/"
          @click.prevent="navigate({
            name: 'accountSettings',
          })"
        >
          Konto Einstellungen
        </router-link>
      </section>
      <section
        class="section"
        v-else
      >
        <a
          href="#"
          @click.prevent="login"
        >
          Login
        </a>
      </section>
      <section
        class="section section--primary"
      >
        <router-link
          to="/"
          @click.prevent="navigate({
            name: 'home',
          })"
        >
          Radio
        </router-link>
        <router-link
          to="/discover/"
          @click.prevent="navigate({
            name: 'discover',
          })"
        >
          Discover
        </router-link>
        <router-link
          to="/collection/"
          @click.prevent="navigate({
            name: 'collection',
          })"
        >
          Favoriten
        </router-link>
      </section>
      <section
        class="section section--primary"
      >
        <router-link
          to="/program/"
          @click.prevent="navigate({
            name: 'program',
          })"
        >
          Programm
        </router-link>
        <router-link
          to="/discover/"
        >
          Empfang
        </router-link>
      </section>
      <section
        class="section"
      >
        <router-link
          to="/history/"
          @click.prevent="navigate({
            path: '/history/',
          })"
          v-text="`History`"
        />
        <router-link
          to="/jobs/"
          @click.prevent="navigate({
            path: '/jobs/',
          })"
          v-text="`Jobs`"
        />
        <router-link
          to="/legal/terms/"
          @click.prevent="navigate({
            path: '/legal/terms/',
          })"
          v-text="`AGB`"
        />
      </section>
      <section
        class="section"
        v-if="user"
      >
        <a
          href="#"
          @click.prevent="logout"
        >
          Abmelden
        </a>
      </section>
    </div>
  </SidePanel>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
@use "@/style/base/typo";
.side-menu {
  .section {
    display: flex;
    flex-direction: column;
    //margin-bottom: 1.5rem;
    padding: 0.5rem 0;
    &:first-child {
      padding-top: 0;
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

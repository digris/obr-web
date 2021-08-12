<script lang="ts">
import { defineComponent, ref } from 'vue';
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
      navigate,
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
        <div
          class="title"
        >Empfang</div>
        <router-link
          to="/"
        >
          dab+
        </router-link>
        <router-link
          to="/discover/"
        >
          Webstream
        </router-link>
      </section>
      <section
        class="section"
      >
        <a
          href="#"
        >
          History
        </a>
        <a
          href="#"
        >
          Jobs
        </a>
        <a
          @click.prevent="logout"
        >
          Logout
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
    margin-bottom: 1.5rem;
    .title {
      @include typo.dim;
    }
    &--primary {
      > a {
        font-size: 4rem;
        line-height: 4.5rem;
      }
    }
    > a {
      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getStaticSrc } from '@/utils/staticfiles';
import { getSocialBackends, disconnectSocialBackend } from '@/api/account';

interface Backend {
  provider: string,
  uid: string,
  connectUrl: string,
  disconnectUrl: string,
  canDisconnect: boolean,
}

export default defineComponent({
  props: {
    next: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const connectedBackends = ref<Array<Backend>>([]);
    const disconnectedBackends = ref<Array<Backend>>([]);
    const fetchBackends = async () => {
      connectedBackends.value = [];
      disconnectedBackends.value = [];
      const backends = await getSocialBackends();
      connectedBackends.value = backends.connected;
      disconnectedBackends.value = backends.disconnected;
    };
    const getProviderLogo = (provider: string) => {
      const key = provider.split('-')[0];
      return getStaticSrc(`assets/brand-icons/${key}.svg`);
    };
    const getProviderText = (provider: string) => {
      const key = provider.split('-')[0];
      // return key.charAt(0).toUpperCase() + key.slice(1);
      return `${key.charAt(0).toUpperCase().toUpperCase()}${key.slice(1)}`;
    };
    const beginLogin = (backend: Backend) => {
      console.debug('beginLogin', backend);
      let nextUrl = backend.connectUrl;
      if (props.next) {
        nextUrl += `?next=${props.next}`;
      }
      console.debug('nextUrl', nextUrl);
      window.location.href = nextUrl;
    };
    const disconnect = async (backend: Backend) => {
      console.debug('disconnect', backend);
      await disconnectSocialBackend(backend.provider, backend.uid);
      await fetchBackends();
    };
    onMounted(fetchBackends);

    return {
      connectedBackends,
      disconnectedBackends,
      beginLogin,
      disconnect,
      getProviderLogo,
      getProviderText,
    };
  },
});
</script>

<template>
  <div
    class="social-login"
  >
    <pre
      class="_debug"
      v-text="disconnectedBackends"
    />
    <pre
      class="_debug"
      v-text="connectedBackends"
    />
    <section
      class="backends backends--disconnected"
    >
      <div
        v-for="backend in disconnectedBackends"
        :key="`disconnected-backend-${backend.provider}`"
        @click="beginLogin(backend)"
        class="backend"
        :class="`backend--${backend.provider}`"
      >
        <img
          class="logo"
          :src="getProviderLogo(backend.provider)"
        />
        <p
          class="name"
        >Continue with {{ getProviderText(backend.provider) }}</p>
      </div>
    </section>
    <section
      class="backends backends--connected"
    >
      <div
        v-for="backend in connectedBackends"
        :key="`connected-backend-${backend.provider}`"
        class="backend"
        :class="`backend--${backend.provider}`"
      >
        <img
          class="logo"
          :src="getProviderLogo(backend.provider)"
        />
        <p
          class="name"
        >
          {{ backend.provider }}
          <br>
          <small class="uid">{{ backend.uid }}</small>
        </p>
        <div
          class="disconnect"
        >
          <button
            @click="disconnect(backend)"
            class="button"
            :class="{'is-disabled': !backend.canDisconnect}"
            :disabled="(!backend.canDisconnect)"
          >disconnect</button>
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
.social-login {
  .backends {
    display: grid;
    grid-gap: 1rem;
    grid-template-columns: repeat(1, 1fr);
    margin-bottom: 2rem;
    @include responsive.bp-small {
      grid-template-columns: repeat(1, 1fr);
    }
  }
  .backend {
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 1rem;
    color: rgb(var(--c-black));
    background: rgb(var(--c-white));
    border: 3px solid rgb(var(--c-black));
    border-radius: 2rem;
    cursor: pointer;
    transition: border-radius 100ms;
    .logo {
      height: 1.5rem;
      margin-right: 1rem;
    }
    .name {
      flex-grow: 1;
      //text-transform: capitalize;
      .uid {
        color: rgba(var(--c-black), 0.5);
        text-transform: lowercase;
      }
    }
    //.disconnect {
    //
    //}
    /*
    &--google-oauth2 {
      border-color: rgba(var(--c-black), 0.5);
    }
    */
    &--facebook {
      color: rgb(var(--c-white));
      background: #1877f2;
      border-color: #1877f2;
    }
    &:hover {
      border-radius: 4px;
    }
  }
}
</style>

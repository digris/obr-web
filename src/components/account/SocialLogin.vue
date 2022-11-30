<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { getSocialBackends, disconnectSocialBackend } from "@/api/account";
import { useDevice } from "@/composables/device";
import imgApple from "@/assets/brand-icons/apple.svg";
import imgGoogle from "@/assets/brand-icons/google.svg";
import imgSpotify from "@/assets/brand-icons/spotify.svg";
import imgDeezer from "@/assets/brand-icons/deezer.svg";

const ICONS = {
  apple: imgApple,
  google: imgGoogle,
  spotify: imgSpotify,
  deezer: imgDeezer,
};

interface Backend {
  provider: string;
  uid: string;
  connectUrl: string;
  disconnectUrl: string;
  canDisconnect: boolean;
}

export default defineComponent({
  props: {
    next: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const { isApp } = useDevice();
    const authBackends = ref<Array<Backend>>([]);
    const fetchBackends = async () => {
      authBackends.value = [];
      const backends = await getSocialBackends();
      authBackends.value = backends.auth;
    };
    const getProviderLogo = (provider: string) => {
      const key = provider.split("-")[0];
      return ICONS[key];
    };
    const getProviderText = (provider: string) => {
      const key = provider.split("-")[0];
      return `${key.charAt(0).toUpperCase().toUpperCase()}${key.slice(1)}`;
    };
    const beginLogin = (backend: Backend) => {
      const connectUrl = backend.connectUrl;
      const params: { [x: string]: string } = {};
      if (props.next) {
        params.next = props.next;
      }
      if (isApp) {
        params.source = "app";
      }
      const q = new URLSearchParams(params).toString();
      const location = q ? `${connectUrl}?${q}` : connectUrl;

      if (isApp) {
        window.appBridge?.send("browser:navigate", {
          url: `${document.location.origin}${location}`,
        });
        return;
      }

      window.location.href = location;
    };
    const disconnect = async (backend: Backend) => {
      await disconnectSocialBackend(backend.provider, backend.uid);
      await fetchBackends();
    };
    onMounted(fetchBackends);

    return {
      authBackends,
      beginLogin,
      disconnect,
      getProviderLogo,
      getProviderText,
    };
  },
});
</script>

<template>
  <div class="social-login">
    <section v-if="authBackends.length" class="backends backends--disconnected">
      <div
        v-for="backend in authBackends"
        :key="`disconnected-backend-${backend.provider}`"
        @click="beginLogin(backend)"
        class="backend"
        :class="`backend--${backend.provider}`"
      >
        <img class="logo" :src="getProviderLogo(backend.provider)" />
        <i18n-t keypath="account.auth.social.continueWith" tag="div" class="title">
          {{ getProviderText(backend.provider) }}
        </i18n-t>
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
    grid-template-columns: repeat(2, 1fr);
    margin-bottom: 2rem;
    @include responsive.bp-medium {
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
      .uid {
        color: rgba(var(--c-black), 0.5);
        text-transform: lowercase;
      }
    }
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

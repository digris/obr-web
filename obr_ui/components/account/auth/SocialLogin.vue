<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import { refAutoReset } from "@vueuse/core";

import { disconnectSocialBackend, getSocialBackends } from "@/api/account";
import imgApple from "@/assets/brand-icons/apple.svg";
import imgDeezer from "@/assets/brand-icons/deezer.svg";
import imgGoogle from "@/assets/brand-icons/google.svg";
import imgSpotify from "@/assets/brand-icons/spotify.svg";
import IconLoading from "@/components/ui/icon/IconBuffering.vue";
import { useDevice } from "@/composables/device";

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
  components: {
    IconLoading,
  },
  props: {
    next: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const { isApp, appVersion } = useDevice();
    const authBackends = ref<Array<Backend>>([]);
    const iOSMaskVisible = refAutoReset(false, 5000);
    const fetchBackends = async () => {
      authBackends.value = [];
      const backends = await getSocialBackends();
      authBackends.value = backends.auth;
    };
    const availableBackends = computed(() => {
      // NOTE: temporarily disable oauth2 for app versions prior to 1.0.1
      if (isApp && appVersion?.major !== 1) {
        return authBackends.value.filter((b) => b.provider !== "google-oauth2");
      }
      // NOTE: temporarily disable apple-id for app-mode
      if (isApp) {
        return authBackends.value.filter((b) => b.provider !== "apple-id");
      }
      return authBackends.value;
    });
    const getProviderLogo = (provider: string) => {
      const key = provider.split("-")[0];
      return ICONS[key];
    };
    const getProviderText = (provider: string) => {
      const key = provider.split("-")[0];
      return `${key.charAt(0).toUpperCase()}${key.slice(1)}`;
    };
    const beginLogin = async (backend: Backend) => {
      if (isApp && backend.provider === "google-oauth2") {
        console.debug("continue with app native google login");
        iOSMaskVisible.value = true;
        window.appBridge?.send("googleSignin:start");
        return;
      }

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
        window.appBridge.pauseHeartbeat();
        iOSMaskVisible.value = true;
        setTimeout(() => {
          window.location.href = location;
        }, 200);
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
      availableBackends,
      beginLogin,
      disconnect,
      getProviderLogo,
      getProviderText,
      iOSMaskVisible,
    };
  },
});
</script>

<template>
  <div class="social-login">
    <section
      v-if="availableBackends.length"
      class="backends backends--disconnected"
      :style="{
        '--num-backends': availableBackends.length,
      }"
    >
      <div
        v-for="backend in availableBackends"
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
    <section v-else class="backends backends--loading">
      <IconLoading />
    </section>
    <transition name="fade">
      <!-- NOTE: mask is displayed to give visual feedback on iOS with apple login.
                 after initiating apple login there is a delay of 1-5s so without feedback
                 it feels like "hanging". -->
      <div v-if="iOSMaskVisible" class="ios-mask" />
    </transition>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

.social-login {
  .backends {
    min-height: 48px;
    display: grid;
    grid-gap: 1rem;
    grid-template-columns: repeat(2, 1fr);
    margin-bottom: 2rem;

    @include responsive.bp-medium {
      grid-template-columns: repeat(1, 1fr);

      // min-height: 108px;

      min-height: calc(var(--num-backends) * 54px);
    }

    &--loading {
      display: flex;
      align-items: center;
      justify-content: center;
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
        color: rgb(var(--c-dark) / 50%);
        text-transform: lowercase;
      }
    }

    &--facebook {
      color: rgb(var(--c-light));
      background: #1877f2;
      border-color: #1877f2;
    }

    @include responsive.on-hover {
      border-radius: 4px;
    }
  }

  .ios-mask {
    top: 0;
    left: 0;
    position: fixed;
    background: rgba(var(--c-light) / 70%);
    height: 100%;
    width: 100%;
    z-index: 99;
  }
}

// mask transitions
.fade-enter-active,
.fade-leave-active {
  transition: opacity 500ms;
}

.fade-enter-from {
  opacity: 0;
}

.fade-leave-to {
  opacity: 0;
}
</style>

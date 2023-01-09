<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { disconnectSocialBackend, getSocialBackends } from "@/api/account";
import imgApple from "@/assets/brand-icons/apple.svg";
import imgDeezer from "@/assets/brand-icons/deezer.svg";
import imgGoogle from "@/assets/brand-icons/google.svg";
import imgSpotify from "@/assets/brand-icons/spotify.svg";

import Section from "./Section.vue";

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

const getProviderText = (provider: string) => {
  const key = provider.split("-")[0];
  return `${key.charAt(0).toUpperCase().toUpperCase()}${key.slice(1)}`;
};

const getProviderLogo = (provider: string) => {
  const key = provider.split("-")[0];
  // @ts-ignore
  return ICONS[key];
};

const annotateBackends = (backends: Backend[]) => {
  return backends.map((b: Backend) => {
    return {
      ...b,
      title: getProviderText(b.provider),
      image: getProviderLogo(b.provider),
    };
  });
};

export default defineComponent({
  components: {
    Section,
  },
  props: {
    next: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const connected = ref<Array<Backend>>([]);
    const auth = ref<Array<Backend>>([]);
    const sync = ref<Array<Backend>>([]);
    const fetchBackends = async () => {
      connected.value = [];
      auth.value = [];
      sync.value = [];
      const backends = await getSocialBackends();
      // in the API we get all AUTH enabled backend - as it is the same endpoint as used during
      // login. so we have to remove the already connected backends here:
      const connectedProviders = backends.connected.map((be: Backend) => be.provider);
      const disconnectedAuth = backends.auth.filter(
        (be: Backend) => !connectedProviders.includes(be.provider)
      );
      connected.value = annotateBackends(backends.connected);
      auth.value = annotateBackends(disconnectedAuth);
      sync.value = annotateBackends(backends.sync);
    };
    const beginLogin = (backend: Backend) => {
      let nextUrl = backend.connectUrl;
      if (props.next) {
        nextUrl += `?next=${props.next}`;
      }
      window.location.href = nextUrl;
    };
    const disconnect = async (backend: Backend) => {
      await disconnectSocialBackend(backend.provider, backend.uid);
      await fetchBackends();
    };
    onMounted(fetchBackends);

    return {
      t,
      connected,
      auth,
      sync,
      beginLogin,
      disconnect,
    };
  },
});
</script>

<template>
  <Section :outlined="false" :title="t('account.settings.social.title')">
    <div class="info">
      <p v-text="t('account.settings.social.info')" />
    </div>
    <div
      v-for="backend in connected"
      :key="`auth-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img class="logo" :src="backend.image" />
      <p class="title">
        {{ backend.title }}
        <span v-if="backend.uid" class="uid" v-text="backend.uid" />
      </p>
      <button
        @click="disconnect(backend)"
        class="button"
        :class="{ 'is-disabled': !backend.canDisconnect }"
        :disabled="!backend.canDisconnect"
        v-text="t('account.settings.social.disconnect')"
      />
    </div>
  </Section>
  <Section :outlined="false" :title="t('account.settings.social.loginAccounts.title')">
    <div
      v-for="backend in auth"
      :key="`auth-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img class="logo" :src="backend.image" />
      <p class="title" v-text="backend.title" />
      <button
        @click="beginLogin(backend)"
        class="button"
        v-text="t('account.settings.social.connect')"
      />
    </div>
  </Section>
  <Section :outlined="false" :title="t('account.settings.social.streamingAccounts.title')">
    <div class="info">
      <p v-text="t('account.settings.social.streamingAccounts.info')" />
    </div>
    <div
      v-for="backend in sync"
      :key="`auth-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img class="logo" :src="backend.image" />
      <p class="title" v-text="backend.title" />
      <button
        @click="beginLogin(backend)"
        class="button"
        v-text="t('account.settings.social.connect')"
      />
    </div>
  </Section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";

.info {
  padding: 0.5rem 2rem 1rem 0;
  opacity: 0.5;
  @include responsive.bp-medium {
    @include typo.small;
  }
}

.backend {
  display: grid;
  grid-template-columns: 32px auto 120px;
  align-items: center;
  margin-bottom: 0.5rem;
  padding: 0.25rem 0.25rem 0.25rem 1rem;
  color: rgb(var(--c-dark));
  border: 1px solid rgb(var(--c-dark) / 20%);
  border-radius: 3px;

  [data-theme="dark"] & {
    border-color: rgb(var(--c-dark) / 5%);
    background: rgb(var(--c-dark) / 5%);
  }

  &:hover {
    background: rgb(var(--c-dark) / 10%);
  }

  .logo {
    height: 1.5rem;
    margin-right: 1rem;
  }

  .title {
    flex-grow: 1;
    line-height: 1rem;

    .uid {
      @include typo.small;
      @include typo.dim;

      margin-left: 0.5rem;
      @include responsive.bp-medium {
        display: none;
        margin-left: 0;
      }
    }
  }

  .button {
    min-width: 120px;
    padding: 0.75rem 1.5rem;
    background: rgb(var(--c-dark) / 10%);
    border: 0;
    cursor: pointer;
    color: rgb(var(--c-dark));

    [data-theme="dark"] & {
      background: rgb(var(--c-dark) / 10%);
    }

    &:disabled {
      cursor: not-allowed;
    }
  }

  /*
  &--spotify {
    color: rgb(var(--c-light));
    background: #1877f2;
    border-color: #1877f2;
  }
  */
}
</style>

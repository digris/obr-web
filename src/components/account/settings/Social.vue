<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";

import Section from "./Section.vue";
import { disconnectSocialBackend, getSocialBackends } from "@/api/account";

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
  <Section title="Verbundene Accounts" :outlined="false">
    <div class="info">
      <p>
        Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.
        <br />Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes.
      </p>
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
        v-text="`trennen`"
      />
    </div>
  </Section>
  <Section title="Login Konten" :outlined="false">
    <div
      v-for="backend in auth"
      :key="`auth-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img class="logo" :src="backend.image" />
      <p class="title" v-text="backend.title" />
      <button @click="beginLogin(backend)" class="button" v-text="`verbinden`" />
    </div>
  </Section>
  <Section title="Streaming Konten" :outlined="false">
    <div class="info">
      <p>
        Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.
      </p>
    </div>
    <div
      v-for="backend in sync"
      :key="`auth-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img class="logo" :src="backend.image" />
      <p class="title" v-text="backend.title" />
      <button @click="beginLogin(backend)" class="button" v-text="`verbinden`" />
    </div>
  </Section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
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
  color: rgb(var(--c-black));
  border: 1px solid rgb(var(--c-gray-200));
  border-radius: 3px;
  &:hover {
    background: rgba(var(--c-black), 0.1);
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
        margin-left: 0;
      }
    }
  }
  .button {
    min-width: 120px;
    padding: 0.75rem 1.5rem;
    background: rgba(var(--c-black), 0.1);
    border: 0;
    cursor: pointer;
    color: rgb(0, 0, 0);
    &:disabled {
      cursor: not-allowed;
    }
  }
  /*
  &--spotify {
    color: rgb(var(--c-white));
    background: #1877f2;
    border-color: #1877f2;
  }
  */
}
</style>

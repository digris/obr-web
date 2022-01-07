<script lang="ts">
import {
  defineComponent, onMounted, ref,
} from 'vue';

import Section from './Section.vue';
import { disconnectSocialBackend, getSocialBackends } from '@/api/account';
import { getStaticSrc } from '@/utils/staticfiles';

interface Backend {
  provider: string,
  uid: string,
  connectUrl: string,
  disconnectUrl: string,
  canDisconnect: boolean,
}

const getProviderText = (provider: string) => {
  const key = provider.split('-')[0];
  return `${key.charAt(0).toUpperCase().toUpperCase()}${key.slice(1)}`;
};

const getProviderLogo = (provider: string) => {
  const key = provider.split('-')[0];
  return getStaticSrc(`assets/brand-icons/${key}.svg`);
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
    const disconnected = ref<Array<Backend>>([]);
    const fetchBackends = async () => {
      connected.value = [];
      disconnected.value = [];
      const backends = await getSocialBackends();
      connected.value = annotateBackends(backends.connected);
      disconnected.value = annotateBackends(backends.disconnected);
    };
    const beginLogin = (backend: Backend) => {
      console.debug('beginLogin', backend);
      let nextUrl = backend.connectUrl;
      if (props.next) {
        nextUrl += `?next=${props.next}`;
      }
      window.location.href = nextUrl;
    };
    const disconnect = async (backend: Backend) => {
      console.debug('disconnect', backend);
      await disconnectSocialBackend(backend.provider, backend.uid);
      await fetchBackends();
    };
    onMounted(fetchBackends);

    return {
      connected,
      disconnected,
      beginLogin,
      disconnect,
    };
  },
});
</script>

<template>
  <Section
    title="Verbundene Konten"
    :outlined="(false)"
  >
    <div
      v-for="backend in connected"
      :key="`disconnected-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img
        class="logo"
        :src="backend.image"
      />
      <p
        class="title"
      >
        {{ backend.title }}
        <span
          v-if="backend.uid"
          class="uid"
          v-text="backend.uid"
        />
      </p>
      <button
        @click="disconnect(backend)"
        class="button"
        :class="{'is-disabled': !backend.canDisconnect}"
        :disabled="(!backend.canDisconnect)"
        v-text="`trennen`"
      />
    </div>
  </Section>
  <Section
    title="Weitere Konten"
    :outlined="(false)"
  >
    <div
      v-for="backend in disconnected"
      :key="`disconnected-backend-${backend.provider}`"
      class="backend"
      :class="`backend--${backend.provider}`"
    >
      <img
        class="logo"
        :src="backend.image"
      />
      <p
        class="title"
        v-text="backend.title"
      />
      <button
        @click="beginLogin(backend)"
        class="button"
        v-text="`verbinden`"
      />
    </div>
  </Section>
</template>

<style lang="scss" scoped>
.backend {
  display: flex;
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
    .uid {
      margin-left: 0.5rem;
      font-size: 0.75rem;
      opacity: 0.5;
    }
  }
  .button {
    min-width: 120px;
    padding: 0.75rem 1.5rem;
    background: rgba(var(--c-black), 0.1);
    border: 0;
    cursor: pointer;
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

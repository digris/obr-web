<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { requireSubscription } from '@/utils/account';
import { getMedia } from '@/api/catalog';
import { getContrastColor } from '@/utils/color';
import eventBus from '@/eventBus';
import ButtonPlay from '@/components/player/button/ButtonPlay.vue';

export default defineComponent({
  components: {
    ButtonPlay,
  },
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
    size: {
      type: Number,
      default: 48,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    backgroundColor: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const store = useStore();
    const playerState = computed(() => store.getters['player/playerState']);
    // const playState = computed(() => store.getters['player/playState']);
    const color = computed(() => store.getters['player/color']);
    const scope = computed(() => store.getters['player/scope']);
    const inScope = computed(() => {
      return scope.value.includes(props.objKey);
    });
    // handle icon / play-state
    const isPlaying = computed(() => {
      return (inScope.value && playerState.value.isPlaying);
    });
    const isBuffering = computed(() => {
      return (inScope.value && playerState.value.isBuffering);
    });
    const buttonCssVars = computed(() => {
      if (inScope.value && color.value) {
        return {
          '--c-fg': color.value.join(','),
        };
      }
      return {
        '--c-fg': '0,0,0',
      };
    });
    const buttonColor = computed(() => {
      if (inScope.value && color.value) {
        return getContrastColor(color.value);
      }
      return [0, 0, 0];
    });
    // handle playlist loading
    const isLoading = ref(false);
    const play = requireSubscription(async () => {
      isLoading.value = true;
      const filter = { ...props.filter };
      if (props.objKey) {
        filter.obj_key = props.objKey;
      }
      const { results } = await getMedia(100, 0, filter);
      const payload = {
        mode: 'replace',
        media: results,
        scope: (props.objKey) ? [props.objKey] : null,
      };
      eventBus.emit('queue:controls:enqueue', payload);
      isLoading.value = false;
    }, 'Subscription required.');
    return {
      play,
      isPlaying,
      isBuffering,
      isLoading,
      inScope,
      buttonCssVars,
      buttonColor,
    };
  },
});
</script>

<template>
  <div
    class="play-action"
  >
    <div
      @click="play"
      class="container"
    >
      <slot
        name="default"
      >
        <ButtonPlay
          :is-active="(inScope)"
          :is-playing="isPlaying"
          :is-buffering="(isLoading || isBuffering)"
          :size="size"
          :outlined="outlined"
          :style="buttonCssVars"
          :color="`rgb(${buttonColor.join(',')})`"
          :backgroundColor="backgroundColor"
        />
      </slot>
    </div>
  </div>
</template>

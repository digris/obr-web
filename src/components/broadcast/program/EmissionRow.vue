<script lang="ts">
import {
  computed,
  defineComponent,
  ref,
  onMounted,
  onUnmounted,
} from 'vue';
import { DateTime } from 'luxon';

export default defineComponent({
  props: {
    emission: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const now = ref(DateTime.now());
    const timer = ref(null);
    const isPast = computed(() => {
      return props.emission.timeEnd < now.value;
    });
    const isUpcoming = computed(() => {
      return props.emission.timeStart > now.value;
    });
    const isCurrent = computed(() => {
      return props.emission.timeStart < now.value && props.emission.timeEnd > now.value;
    });
    const cssVars = computed(() => {
      if (isCurrent.value) {
        return {
          '--c-fg': 'var(--c-white)',
          '--c-bg': 'var(--c-black)',
        };
      }
      if (isPast.value) {
        return {
          '--c-fg': 'var(--c-black)',
          '--c-bg': 'var(--c-gray-50)',
        };
      }
      return {
        '--c-fg': 'var(--c-black)',
        '--c-bg': 'var(--c-white)',
      };
    });
    onMounted(() => {
      // @ts-ignore
      timer.value = setInterval(() => {
        now.value = DateTime.now();
      }, 2000);
    });
    onUnmounted(() => {
      // @ts-ignore
      clearInterval(timer.value);
    });
    const tagsDisplay = computed(() => {
      return props.emission.tags.slice(0, 4).join(', ');
    });
    const timeStartDisplay = computed(() => {
      if (!props.emission?.timeStart) {
        return null;
      }
      return props.emission.timeStart.setLocale('de-ch').toLocaleString(DateTime.TIME_24_SIMPLE);
    });
    return {
      cssVars,
      isPast,
      isCurrent,
      isUpcoming,
      tagsDisplay,
      timeStartDisplay,
    };
  },
});
</script>

<template>
  <div
    class="emission-row"
    :style="cssVars"
    :class="{
      'is-past': isPast,
      'is-current': isCurrent,
      'is-upcoming': isUpcoming,
    }"
  >
    <div
      class="container"
    >
      <div
        class="play"
      >
        ( P )
      </div>
      <div
        class="name"
      >
        <router-link
          :to="{
            name: 'playlistDetail',
            params: {
              uid: emission.uid,
            },
          }"
          v-text="(emission.series || emission.name)"
        />
      </div>
      <div
        class="editor"
      >
        {{ emission.editor }}
      </div>
      <div
        class="tags"
      >
        {{ tagsDisplay }}
      </div>
      <div
        class="time-start"
      >
        {{ timeStartDisplay }}
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";

.emission-row {
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;
  color: rgb(var(--c-fg));
  background-color: rgb(var(--c-bg));

  &:first-child {
    border-top: 1px solid rgb(var(--c-gray-200));
  }

  &:hover {
    background: rgb(var(--c-gray-100));
  }
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor  time-start"
    "play name tags    time-start";
  grid-template-columns: 1fr 9fr 8fr 2fr;
  padding: 0.75rem 0;

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    position: relative;
    grid-area: play;
  }

  .name {
    grid-area: name;
    @include typo.large;
    min-width: 0;
    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .editor {
    grid-area: editor;
    overflow: hidden;
  }

  .tags {
    grid-area: tags;
  }

  .time-start {
    grid-area: time-start;
    @include typo.large;
    justify-content: flex-end;
  }
}
</style>

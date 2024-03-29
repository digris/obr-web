<script lang="ts">
import type { PropType } from "vue";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import type { ScheduleEmission, SchedulePlaylist } from "@/typings/api";

export default defineComponent({
  props: {
    emission: {
      type: Object as PropType<ScheduleEmission>,
      required: true,
    },
    playlist: {
      type: Object as PropType<SchedulePlaylist>,
      required: true,
    },
  },
  setup(props) {
    const { t } = useI18n();
    const link = computed(() => {
      return {
        name: "playlistDetail",
        params: {
          uid: props.playlist.uid,
        },
      };
    });
    const titleDisplay = computed(() => {
      const name = props.playlist?.series?.name || props.playlist.name;
      const appendix = props.playlist?.series?.episode;
      return name && appendix ? `${name} #${appendix}` : name;
    });
    const editorDisplay = computed(() => {
      return props.playlist?.editor?.name ?? "";
    });
    return {
      t,
      link,
      titleDisplay,
      editorDisplay,
    };
  },
});
</script>

<template>
  <router-link :to="link" class="focused-emission">
    <div class="title">
      <span class="label">{{ t("catalog.ct.playlist") }}: </span>
      {{ titleDisplay }}
    </div>
    <div v-if="editorDisplay" class="editor">
      <span class="label">by </span>
      {{ editorDisplay }}
    </div>
  </router-link>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.focused-emission {
  max-width: 100%;
  line-height: 20px;

  .title,
  .editor {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .title {
    &::first-letter {
      text-transform: uppercase;
    }
  }
}
</style>

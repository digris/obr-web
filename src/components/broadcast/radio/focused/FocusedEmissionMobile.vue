<script lang="ts">
import type { PropType } from "vue";
import type { ScheduleEmission, SchedulePlaylist } from "@/typings/api";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

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
    <div class="title">{{ t("catalog.ct.playlist") }}: {{ titleDisplay }}</div>
    <div v-if="editorDisplay" class="editor">by {{ editorDisplay }}</div>
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

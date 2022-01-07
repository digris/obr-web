<script lang="ts">
import { defineComponent } from 'vue';
import CircleProgressButton from '@/components/ui/button/CircleProgressButton.vue';
import IconPlay from '@/components/ui/icon/IconPlay.vue';
import IconPlaying from '@/components/ui/icon/IconPlaying.vue';

export default defineComponent({
  components: {
    CircleProgressButton,
    IconPlay,
    IconPlaying,
  },
});
</script>
<template>
  <div
    class="ptype-view"
  >
    <div
      class="stage"
    >
      <CircleProgressButton
        :size="(64)"
        :outline-width="(4)"
        :progress="(0.5)"
      >
        <span>X</span>
      </CircleProgressButton>
      <CircleProgressButton
        :size="(36)"
        :outline-width="(2)"
        :progress="(0.5)"
      />
      <CircleProgressButton
        :size="(48)"
        :outline-width="(4)"
        :progress="(0.5)"
      >
        <IconPlay
          :size="(48)"
        />
      </CircleProgressButton>
      <CircleProgressButton
        :size="(96)"
        :outline-width="(6)"
        :progress="(0.5)"
        :filled="(true)"
      >
        <IconPlaying
          :size="(96)"
        />
      </CircleProgressButton>
      <CircleProgressButton
        :size="(96)"
        :outline-width="(6)"
        :progress="(0.5)"
        color-var="--c-black"
      >
        <IconPlaying
          :size="(96)"
          color="rgb(var(--c-black))"
        />
      </CircleProgressButton>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.ptype-view {
  background: rgb(var(--white));
}
.stage {
  padding: 2rem;
}
</style>

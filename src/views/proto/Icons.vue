<script lang="ts">
import { defineComponent } from "vue";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconLogo from "@/components/ui/icon/IconLogo.vue";
import IconPType from "@/components/ui/icon/IconPType.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconPType,
    IconLogo,
  },
  setup() {
    const stageVarsA = {
      "--c-fg": "0,0,0",
      "--c-fg-inverse": "255,255,255",
      "--c-bg": "200,255,255",
      "--c-active": "255,0,255",
    };
    const stageVarsB = {
      "--c-fg": "255,255,255",
      "--c-fg-inverse": "0,0,0",
      "--c-bg": "0,0,0",
      "--c-active": "255,255,0",
    };
    return {
      stageVarsA,
      stageVarsB,
    };
  },
});
</script>
<template>
  <div class="ptype-view">
    <div class="stage typo">
      <p class="t t--wf t--500">Foo the Bear 500</p>
      <p class="t t--alt t--500">Foo the Bear 500 (alt)</p>
    </div>
    <div class="stage" :style="stageVarsA">
      <pre v-text="stageVarsA" />
      <div class="row">
        <div>
          <CircleButton
            :outlined="true"
            :outline-width="2"
            :outline-opacity="1"
            :outline-on-hover="true"
          >
            <IconLogo :scale="1" />
          </CircleButton>
        </div>
        <div>
          <CircleButton
            :outlined="true"
            :outline-width="3"
            :outline-opacity="1"
            :outline-on-hover="true"
            :scale="2"
          >
            <IconLogo :scale="2" mode="play" />
          </CircleButton>
        </div>
        <div>
          <CircleButton
            :outlined="true"
            :outline-width="2"
            :outline-opacity="1"
            :outline-on-hover="true"
          >
            <IconLogo :scale="1" mode="pause" />
          </CircleButton>
        </div>
        <div>
          <CircleButton
            :outlined="true"
            :outline-width="2"
            :outline-opacity="1"
            :outline-on-hover="true"
          >
            <IconLogo :scale="1" mode="playing" />
          </CircleButton>
        </div>
      </div>
    </div>
    <div class="stage" :style="stageVarsA">
      <pre v-text="stageVarsA" />
      <div class="row">
        <div>
          <CircleButton>
            <IconPType />
          </CircleButton>
        </div>
        <div>
          <CircleButton :outlined="true">
            <IconPType />
          </CircleButton>
        </div>
        <div>
          <CircleButton :disabled="true">
            <IconPType />
          </CircleButton>
        </div>
        <div>
          <CircleButton :filled="true" :hover-background-opacity="0.6">
            <IconPType color-var="--c-white" />
          </CircleButton>
        </div>
        <div>
          <CircleButton :filled="true" fill-color-var="--c-active" :hover-background-opacity="0.9">
            <IconPType color-var="--c-white" />
          </CircleButton>
        </div>
        <div>
          <CircleButton :filled="true" :hover-background-opacity="0.9">
            <IconPType color-var="--c-red" />
          </CircleButton>
        </div>
        <div>
          <CircleButton :scale="2" :outlined="true">
            <IconPType :scale="1.5" />
          </CircleButton>
        </div>
      </div>
    </div>
    <div class="stage" :style="stageVarsB">
      <pre v-text="stageVarsB" />
      <div class="row">
        <div>
          <CircleButton>
            <IconPType />
          </CircleButton>
        </div>
        <div>
          <CircleButton :outlined="true">
            <IconPType />
          </CircleButton>
        </div>
        <div>
          <CircleButton :disabled="true">
            <IconPType />
          </CircleButton>
        </div>
        <div>
          <CircleButton :filled="true" :hover-background-opacity="0.6">
            <IconPType color-var="--c-black" />
          </CircleButton>
        </div>
        <div>
          <CircleButton :filled="true" fill-color-var="--c-active" :hover-background-opacity="0.6">
            <IconPType color-var="--c-black" />
          </CircleButton>
        </div>
      </div>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.ptype-view {
  background: rgb(var(--white));
}

.stage {
  padding: 2rem;
  background: rgb(var(--c-bg));

  .row {
    border-bottom: 1px solid #a9a9a9;
    padding: 2rem 0;
    display: grid;
    grid-gap: 2rem;
    grid-template-columns: repeat(auto-fill, 64px);
  }
}

.t {
  font-size: 24px;

  &--500 {
    font-weight: 500;
  }
}
</style>

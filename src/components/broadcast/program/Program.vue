<script lang="ts">
import { defineComponent, computed, onMounted, onActivated } from "vue";
import { useStore } from "vuex";
import Emission from "./Emission.vue";

export default defineComponent({
  components: {
    Emission,
  },
  props: {
    currentLinkToHome: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["navigate"],
  setup(props, { emit }) {
    const store = useStore();
    const emissions = computed(() => store.getters["program/emissions"]);
    onMounted(() => {
      store.dispatch("program/loadProgram");
    });
    onActivated(() => {
      store.dispatch("program/loadProgram");
    });
    const navigate = () => {
      emit("navigate");
    };
    return {
      emissions,
      navigate,
    };
  },
});
</script>
<template>
  <div class="program">
    <Emission
      v-for="(emission, index) in emissions"
      :key="`program-emission-${emission.uid}-${index}`"
      :emission="emission"
      :current-link-to-home="currentLinkToHome"
      @navigate="navigate"
    />
  </div>
</template>

<style lang="scss" scoped>
/*
.program {
  .emission-row {
    &:first-child {
      border-top: 0;
    }
  }
}
*/
.body {
  background: rgb(var(--white));
}
</style>

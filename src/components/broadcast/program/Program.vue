<script lang="ts">
import {
  defineComponent,
  computed,
  onMounted,
  onActivated,
} from 'vue';
import { useStore } from 'vuex';
import Emission from './Emission.vue';

export default defineComponent({
  components: {
    Emission,
  },
  setup() {
    const store = useStore();
    const emissions = computed(() => store.getters['program/emissions']);
    onMounted(() => {
      store.dispatch('program/loadProgram');
    });
    onActivated(() => {
      store.dispatch('program/loadProgram');
    });
    return {
      emissions,
    };
  },
});
</script>
<template>
  <div
    class="program"
  >
    <Emission
      v-for="(emission, index) in emissions"
      :key="`program-emission-${emission.uid}-${index}`"
      :emission="emission"
    />
  </div>
</template>

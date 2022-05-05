import { computed } from "vue";
import { useStore } from "vuex";

const useStreamSettings = () => {
  const store = useStore();
  const maxBandwidth = computed(() => store.getters["settings/maxBandwidth"]);
  const setMaxBandwidth = async (value: number) => {
    await store.dispatch("settings/setMaxBandwidth", value);
  };
  return {
    maxBandwidth,
    setMaxBandwidth,
  };
};

export { useStreamSettings };

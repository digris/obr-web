import { computed } from "vue";
import { useStore } from "vuex";

const useTime = () => {
  const store = useStore();
  const stationTime = computed(() => store.getters["time/stationTime"]);
  const playheadTime = computed(() => store.getters["time/playheadTime"]);
  const time = computed(() => store.getters["time/time"]);
  return {
    stationTime,
    playheadTime,
    time,
  };
};

export { useTime };

import { defineStore } from "pinia";
import { DateTime } from "luxon";

interface State {
  stationTime: DateTime;
}

export const useTimeStore = defineStore("time", {
  state: (): State => ({
    stationTime: DateTime.now(),
  }),
  getters: {
    time(state) {
      return state.stationTime;
    },
  },
  actions: {
    syncStationTime() {
      this.stationTime = DateTime.now();
    },
  },
});

setInterval(() => {
  const { syncStationTime } = useTimeStore();
  syncStationTime();
}, 200);

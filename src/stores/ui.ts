import { defineStore } from "pinia";

type RGBColor = Array<number>;

interface State {
  primaryColor: RGBColor;
  playerVisible: boolean;
  filterExpanded: boolean;
}

export const useUiStore = defineStore("ui", {
  state: (): State => ({
    primaryColor: [0, 0, 0],
    playerVisible: true,
    filterExpanded: false,
  }),
  actions: {
    setPrimaryColor(value: Array<number>) {
      this.primaryColor = value;
    },
  },
});

import { defineStore } from "pinia";

type RGBColor = Array<number>;

interface State {
  primaryColor: RGBColor;
  playerVisible: boolean;
  filterExpanded: boolean;
  vpWidth: number;
  vpHeight: number;
}

export const useUiStore = defineStore("ui", {
  state: (): State => ({
    primaryColor: [0, 0, 0],
    playerVisible: false,
    filterExpanded: false,
    vpWidth: window.innerWidth,
    vpHeight: window.innerHeight,
  }),
  actions: {
    setPrimaryColor(value: [number, number, number]): void {
      this.primaryColor = value;
    },
    setWindowSize(size: [number, number]): void {
      this.vpWidth = size[0];
      this.vpHeight = size[1];
    },
  },
});

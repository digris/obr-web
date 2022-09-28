import { defineStore } from "pinia";

interface State {
  filterExpanded: boolean;
}

export const useUiStore = defineStore("ui", {
  state: (): State => ({
    filterExpanded: false,
  }),
});

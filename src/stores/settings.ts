import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";

interface State {
  maxBandwidth: number;
  locale: string;
}

export const useSettingsStore = defineStore("settings", {
  state: (): State => ({
    maxBandwidth: useStorage("settings/stream/maxBandwidth", 200000),
    locale: useStorage("settings/locale", "de"),
  }),
  getters: {
    language(state) {
      return state.locale;
    },
  },
  actions: {
    setLocale(value: string) {
      this.locale = value;
    },
    setMaxBandwidth(value: number) {
      this.maxBandwidth = value;
    },
    resetSettings() {
      this.$reset();
    },
  },
});

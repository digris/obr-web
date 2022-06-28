import { defineStore } from "pinia";
import { useStorage, useNavigatorLanguage } from "@vueuse/core";

interface State {
  volume: number;
  shuffleMode: Boolean;
  maxBandwidth: number;
  locale: string;
}

const getDefaultLanguage = () => {
  const { language } = useNavigatorLanguage();
  return language.value?.substring(0, 2) ?? "de";
};

export const useSettingsStore = defineStore("settings", {
  state: (): State => ({
    volume: useStorage("settings/player/volume", 100),
    shuffleMode: useStorage("settings/player/shuffleMode", false),
    maxBandwidth: useStorage("settings/stream/maxBandwidth", 200000),
    locale: useStorage("settings/locale", getDefaultLanguage()),
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
    setVolume(value: number) {
      this.volume = value;
    },
    setMaxBandwidth(value: number) {
      this.maxBandwidth = value;
    },
    resetSettings() {
      this.$reset();
    },
  },
});

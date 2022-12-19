import { useNavigatorLanguage, useStorage } from "@vueuse/core";
import { defineStore } from "pinia";

interface State {
  darkMode: boolean;
  volume: number;
  shuffleMode: boolean;
  maxBandwidth: number;
  locale: string;
}

const getDefaultLanguage = () => {
  const { language } = useNavigatorLanguage();
  return language.value?.substring(0, 2) ?? "de";
};

export const useSettingsStore = defineStore("settings", {
  state: (): State => ({
    // @ts-ignore
    darkMode: useStorage("settings/darkMode", false),
    // @ts-ignore
    volume: useStorage("settings/player/volume", 100),
    // @ts-ignore
    shuffleMode: useStorage("settings/player/shuffleMode", false),
    // @ts-ignore
    maxBandwidth: useStorage("settings/stream/maxBandwidth", 200000),
    // @ts-ignore
    locale: useStorage("settings/locale", getDefaultLanguage()),
  }),
  getters: {
    language(state) {
      return state.locale;
    },
  },
  actions: {
    setDarkMode(value: boolean) {
      this.darkMode = value;
    },
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

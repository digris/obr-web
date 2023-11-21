import { useNavigatorLanguage, useStorage } from "@vueuse/core";
import { defineStore } from "pinia";

import { useDevice } from "@/composables/device";

interface State {
  darkMode: boolean;
  baseVolume: number;
  shuffleMode: boolean;
  maxBandwidth: number;
  locale: string;
}

const getDefaultLanguage = () => {
  const { language } = useNavigatorLanguage();
  return language.value?.substring(0, 2) ?? "de";
};

const getDefaultDarkMode = () => {
  const { isApp } = useDevice();
  return isApp;
};

export const useSettingsStore = defineStore("settings", {
  state: (): State => ({
    // @ts-ignore
    darkMode: useStorage("settings/darkMode", getDefaultDarkMode()),
    // @ts-ignore
    baseVolume: useStorage("settings/player/baseVolume", 1),
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
    setBaseVolume(value: number) {
      this.baseVolume = value;
    },
    setShuffleMode(value: boolean) {
      this.shuffleMode = value;
    },
    toggleShuffleMode() {
      this.shuffleMode = !this.shuffleMode;
    },
    setMaxBandwidth(value: number) {
      this.maxBandwidth = value;
    },
    resetSettings() {
      this.$reset();
    },
  },
});

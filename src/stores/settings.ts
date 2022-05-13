import { defineStore } from "pinia";
import { useStorage, useNavigatorLanguage } from "@vueuse/core";

interface State {
  maxBandwidth: number;
  locale: string;
}

const getDefaultLanguage = () => {
  const { language } = useNavigatorLanguage();
  return language.value?.substring(0, 2) ?? "de";
};

export const useSettingsStore = defineStore("settings", {
  state: (): State => ({
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
    setMaxBandwidth(value: number) {
      this.maxBandwidth = value;
    },
    resetSettings() {
      this.$reset();
    },
  },
});

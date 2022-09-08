import { defineStore } from "pinia";
import { useStorage, useNavigatorLanguage } from "@vueuse/core";

interface State {
  theme: "light" | "dark" | null;
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
    theme: useStorage("settings/theme", null),
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
    loadSchedule() {
      console.debug("stores/schedule: loadSchedule");
    },
    updateCurrent(current: any) {
      console.debug("stores/schedule: updateCurrent", current);
    },
  },
});

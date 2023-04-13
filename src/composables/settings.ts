import { storeToRefs } from "pinia";

import { useDevice } from "@/composables/device";
import { useAccountStore } from "@/stores/account";
import { useSettingsStore } from "@/stores/settings";

export const useSettings = () => {
  const appBridge = window.appBridge;
  const { isWeb } = useDevice();
  const { locale, darkMode, maxBandwidth, shuffleMode, volume } = storeToRefs(useSettingsStore());
  const { settings: userSettings } = storeToRefs(useAccountStore());
  const {
    setMaxBandwidth: setMaxBandwidthWeb,
    setDarkMode: setDarkModeWeb,
    toggleShuffleMode,
  } = useSettingsStore();

  const setDarkMode = async (value: boolean) => {
    if (isWeb) {
      setDarkModeWeb(value);
    } else {
      const channel = "settings:setDarkMode";
      await appBridge.send(channel, {
        darkMode: value,
      });
      // NOTE: remove after dark-mode setting is implemented in app
      setDarkModeWeb(value);
    }
  };

  const setMaxBandwidth = async (bandwidth: number) => {
    if (isWeb) {
      setMaxBandwidthWeb(bandwidth);
    } else {
      const channel = "settings:setMaxBandwidth";
      await appBridge.send(channel, {
        maxBandwidth: bandwidth,
      });
    }
  };

  return {
    locale,
    darkMode,
    maxBandwidth,
    shuffleMode,
    volume,
    userSettings,
    setDarkMode,
    setMaxBandwidth,
    toggleShuffleMode,
  };
};

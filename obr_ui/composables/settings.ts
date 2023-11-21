import { storeToRefs } from "pinia";

import { useDevice } from "@/composables/device";
import { useAccountStore } from "@/stores/account";
import { useSettingsStore } from "@/stores/settings";

export const useSettings = () => {
  const appBridge = window.appBridge;
  const { isWeb } = useDevice();
  const { locale, darkMode, maxBandwidth, shuffleMode, baseVolume } = storeToRefs(
    useSettingsStore()
  );
  const { settings: userSettings } = storeToRefs(useAccountStore());
  const {
    setMaxBandwidth: setMaxBandwidthWeb,
    setDarkMode,
    toggleShuffleMode,
  } = useSettingsStore();

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
    baseVolume,
    userSettings,
    setDarkMode,
    setMaxBandwidth,
    toggleShuffleMode,
  };
};

import { storeToRefs } from "pinia";

import { useDevice } from "@/composables/device";
import { useSettingsStore } from "@/stores/settings";

export const useSettings = () => {
  const appBridge = window.appBridge;
  const { isWeb } = useDevice();
  const { darkMode, maxBandwidth, volume } = storeToRefs(useSettingsStore());
  const { setMaxBandwidth: setMaxBandwidthWeb, setDarkMode: setDarkModeWeb } = useSettingsStore();

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
    darkMode,
    maxBandwidth,
    volume,
    setDarkMode,
    setMaxBandwidth,
  };
};

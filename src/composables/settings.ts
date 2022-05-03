import { useLocalStorage } from "@vueuse/core";

const useStreamSettings = () => {
  const maxBandwidth = useLocalStorage("stream-max-bw", 0);
  return {
    maxBandwidth,
  };
};

export { useStreamSettings };

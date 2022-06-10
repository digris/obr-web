import { getStreamUrl } from "@/player/stream";

const useStreamControls = () => {
  const audioPlayer = window.audioPlayer;
  const startPlayStream = (startTime = 0) => {
    const url = getStreamUrl();
    audioPlayer.play(url, startTime);
  };
  return {
    startPlayStream,
  };
};

export { useStreamControls };

import eventBus from "@/eventBus";
import { getStreamUrl } from "@/player/stream";

const useStreamControls = () => {
  const startPlayStream = async (startTime = 0) => {
    const url = getStreamUrl();
    const event = {
      do: "play",
      url,
      startTime,
    };
    eventBus.emit("player:controls", event);
  };
  return {
    startPlayStream,
  };
};

export { useStreamControls };

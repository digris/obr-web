import { useDocumentVisibility, useIntervalFn } from "@vueuse/core";

import { sendHeartbeat } from "@/api/stats";
import { usePlayerState } from "@/composables/player";

const HEARTBEAT_INTERVAL = 60 * 1000;

class HeartbeatHandler {
  constructor() {
    useIntervalFn(async () => {
      await this.send();
    }, HEARTBEAT_INTERVAL);
    this.send().then();
  }

  async send() {
    const visibility = useDocumentVisibility();
    const { mode, playState } = usePlayerState();
    const payload = {
      inForeground: visibility.value === "visible",
      playerSource: mode.value,
      playerState: playState.value,
    };
    await sendHeartbeat(payload);
  }
}

export default function () {
  return new HeartbeatHandler();
}

import { computed, watch, ref } from "vue";
import { debounce, isEqual } from "lodash-es";

import { createPlayerEvents } from "@/api/stats";
import { usePlayerState } from "@/composables/player";

export interface Event {
  state: string;
  objKey: string;
  objName: string;
  source: string;
}

const createGA4Event = (event: Event) => {
  const GA4event = {
    event: "player",
    state: event.state,
    source: event.source,
    obj_key: event.objKey,
    obj_name: event.objName,
  };
  // @ts-ignore
  window.dataLayer.push(GA4event);
  console.debug("GA4event", GA4event);
};

class EventHandler {
  queue: Array<Event>;

  constructor() {
    this.queue = [];
    // TODO: fix for pinia
    // const { playState, isLive, media } = usePlayerState();
    const { isLive, playerState } = usePlayerState();
    // const isLive = ref(false);
    const media = ref(null);

    const playState = computed(() => {
      if (playerState.value?.isPlaying) {
        return "playing";
      }
      if (playerState.value?.isPaused) {
        return "paused";
      }
      if (playerState.value?.isBuffering) {
        return "buffering";
      }
      return "stopped";
    });

    const combinedState = computed(() => {
      const objKey = media.value ? `${media.value.ct}:${media.value.uid}` : null;
      return {
        state: playState.value,
        objKey,
        objName: media.value?.name,
        source: isLive.value ? "live" : "on-demand",
      };
    });
    const addEvent = debounce(async (event) => {
      if (!event.objKey) {
        return;
      }
      createGA4Event(event);
      await createPlayerEvents([event]);
    }, 200);
    watch(combinedState, (newState, oldState) => {
      if (isEqual(newState, oldState)) {
        return;
      }
      const event = {
        ...newState,
        ts: new Date().getTime(),
      };
      addEvent(event);
    });
  }
}

export default function () {
  return new EventHandler();
}

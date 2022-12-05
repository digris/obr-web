import { watchThrottled } from "@vueuse/core";
import { debounce, isEqual } from "lodash-es";
import log from "loglevel";
import { computed } from "vue";

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
  log.debug("GA4event", GA4event);
};

class EventHandler {
  queue: Array<Event>;

  constructor() {
    this.queue = [];
    const { media, isLive, state } = usePlayerState();
    const combinedState = computed(() => {
      const objKey = media.value ? `${media.value.ct}:${media.value.uid}` : null;
      return {
        state: state.value,
        objKey,
        objName: media.value?.name,
        source: isLive.value ? "live" : "on-demand",
      };
    });
    const addEvent = debounce(async (event) => {
      if (!event.objKey) {
        return;
      }
      // log.debug("events - addEvent", event);
      createGA4Event(event);
      await createPlayerEvents([event]);
    }, 200);
    /*
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
    */
    watchThrottled(
      combinedState,
      (newValue, oldValue) => {
        if (isEqual(newValue, oldValue)) {
          return;
        }
        const event = {
          ...newValue,
          ts: new Date().getTime(),
        };
        addEvent(event);
      },
      { throttle: 200 }
    );
  }
}

export default function () {
  return new EventHandler();
}

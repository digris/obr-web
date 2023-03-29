import { computed, watch } from "vue";
import log from "loglevel";
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
  log.debug("GA4event", GA4event);
};

class EventHandler {
  constructor() {
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
      log.info("events - addEvent", event);
      createGA4Event(event);
      await createPlayerEvents([event]);
    }, 200);
    watch(combinedState, (newValue, oldValue) => {
      if (isEqual(newValue, oldValue)) {
        return;
      }
      const event = {
        ...newValue,
        ts: new Date().getTime(),
      };
      addEvent(event);
    });
  }
}

export default function () {
  return new EventHandler();
}

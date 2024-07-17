import { computed, watch } from "vue";
import { debounce, isEqual } from "lodash-es";

import { sendPlayerEvent } from "@/analytics/event";
import { createPlayerEvents } from "@/api/stats";
import { usePlayerState } from "@/composables/player";

export interface Event {
  state: string;
  objKey: string;
  objName: string;
  source: string;
}

const createAnalyticsEvent = (event: Event) => {
  sendPlayerEvent({
    state: event.state,
    source: event.source,
    obj_key: event.objKey,
    obj_name: event.objName,
  });
};

class EventHandler {
  constructor() {
    const { media, isLive, playState } = usePlayerState();
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
      createAnalyticsEvent(event);
      await createPlayerEvents([event]);
    }, 2000);
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

import { computed, watch } from "vue";
import { isEqual } from "lodash-es";
import store from "@/store";

class PlayerStateHandler {
  constructor() {
    const state = computed(() => store.getters["player/playerState"]);
    const isLive = computed(() => state.value && state.value.isLive);
    const computedItem = computed(() => {
      if (isLive.value) {
        return {
          isLive: true,
          media: store.getters["schedule/currentMedia"] || null,
        };
      }
      return {
        isLive: false,
        media: store.getters["queue/currentMedia"] || null,
      };
    });
    watch(computedItem, (item, previousItem) => {
      if (isEqual(item, previousItem)) {
        return;
      }
      store.dispatch("player/updateCurrentItem", item);
    });
  }
}

export default function () {
  return new PlayerStateHandler();
}

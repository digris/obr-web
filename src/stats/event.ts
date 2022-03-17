import { computed, watch } from 'vue';
import { debounce, isEqual } from 'lodash-es';
import store from '@/store';

import { createPlayerEvents } from '@/api/stats';

export interface Event {
  state: string,
  objKey: string,
  objName: string,
  source: string,
}

const createGA4Event = (event: Event) => {
  const GA4event = {
    event: 'player',
    state: event.state,
    source: event.source,
    obj_key: event.objKey,
    obj_name: event.objName,
  };
  // @ts-ignore
  window.dataLayer.push(GA4event);
  // console.debug('createGA4Event', event);
};

class EventHandler {
  queue: Array<Event>;

  constructor() {
    this.queue = [];
    const playState = computed(() => store.getters['player/playState']);
    const isLive = computed(() => store.getters['player/isLive']);
    const media = computed(() => store.getters['player/media']);
    const combinedState = computed(() => {
      const objKey = (media.value) ? `${media.value.ct}:${media.value.uid}` : null;
      return {
        state: playState.value,
        objKey,
        objName: media.value?.name,
        source: (isLive.value) ? 'live' : 'on-demand',
      };
    });
    const addEvent = debounce(async (event) => {
      if (!event.objKey) {
        // console.debug('event without objKey', event);
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
      // console.debug('EventHandler', event);
      addEvent(event);
    });
    // watch([playState, media], ([newState, newMedia], [prevState, prevMedia]) => {
    //   let txt = '';
    //   txt += (prevMedia) ? prevMedia.uid : '-';
    //   txt += ' > ';
    //   txt += (newMedia) ? newMedia.uid : '-';
    //   console.debug('EventHandler', `${prevState} > ${newState}`, `${txt}`);
    // });
  }
}

export default function () {
  return new EventHandler();
}

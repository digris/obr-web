import { DateTime } from 'luxon';
import store from '@/store';

const TIME_OFFSET = -20;

class StationTimeHandler {
  constructor() {
    setInterval(async () => {
      const now = DateTime.now().plus({ seconds: TIME_OFFSET });
      await store.dispatch('time/setStationTime', now);
    }, 200);
  }
}

export default function () {
  return new StationTimeHandler();
}

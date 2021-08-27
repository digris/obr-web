import { DateTime } from 'luxon';
import store from '@/store';

class StationTimeHandler {
  constructor() {
    setInterval(async () => {
      await store.dispatch('time/setStationTime', DateTime.now());
    }, 200);
  }
}

export default function () {
  return new StationTimeHandler();
}

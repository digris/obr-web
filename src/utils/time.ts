import store from '@/store';
import { DateTime } from 'luxon';

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

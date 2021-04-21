// @ts-ignore
import scheduler from 'node-schedule';
import store from '@/store';
import { DateTime } from 'luxon';

class StationTimeHandler {
  constructor() {
    const job = scheduler.scheduleJob('* * * * * * ', async () => {
      const now = DateTime.now();
      await store.dispatch('time/setStationTime', now);
    });
  }
}

export default function () {
  return new StationTimeHandler();
}

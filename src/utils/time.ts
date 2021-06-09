// @ts-ignore
import scheduler from 'node-schedule';
import store from '@/store';
import { DateTime } from 'luxon';

const JOB_MAX_AGE = 300;

class StationTimeHandler {
  constructor() {
    const job = scheduler.scheduleJob('* * * * * * ', async (scheduledDate: Date) => {
      // @ts-ignore
      if (scheduledDate && (new Date() - scheduledDate) > JOB_MAX_AGE * 1000) {
        return;
      }
      const now = DateTime.now();
      // await store.dispatch('time/setStationTime', now);
    });
    job.invoke();
    const interval = setInterval(async () => {
      await store.dispatch('time/setStationTime', DateTime.now());
    }, 200);
  }
}

export default function () {
  return new StationTimeHandler();
}

export interface Event {
  ct: string,
  uid: string,
}

class EventHandler {
  queue: Array<Event>;

  constructor() {
    this.queue = [];
  }
}

export default function () {
  return new EventHandler();
}

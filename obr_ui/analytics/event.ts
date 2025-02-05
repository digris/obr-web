export interface PlayerEvent {
  state: string;
  obj_key: string;
  obj_name: string;
  source: string;
}

const sendGA4Event = (GA4Event: object) => {
  // @ts-ignore
  window.dataLayer.push(GA4Event);
};

const sendEvent = () => {
  console.log("sendEvent");
};

const sendPlayerEvent = (event: PlayerEvent) => {
  sendGA4Event({
    event: "player",
    ...event,
  });
};

export { sendEvent, sendPlayerEvent };

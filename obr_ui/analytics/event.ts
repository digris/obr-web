export interface PlayerEvent {
  state: string;
  obj_key: string;
  obj_name: string;
  source: string;
}

export interface AnalyticsEvent {
  kind: string;
  data: object;
}

const sendGA4Event = (GA4Event: object) => {
  // @ts-ignore
  window.dataLayer.push(GA4Event);
};

const sendEvent = (event: AnalyticsEvent) => {
  const { kind, data } = event;
  const ga4Event = {
    event: kind,
    ...data,
  };
  sendGA4Event(ga4Event);
};

const sendPlayerEvent = (event: PlayerEvent) => {
  sendGA4Event({
    event: "player",
    ...event,
  });
};

export { sendEvent, sendPlayerEvent };

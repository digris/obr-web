import { useAccount } from "@/composables/account";

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
  const { user } = useAccount();
  console.debug("GA4Event", {
    ...GA4Event,
    user_id: user.value?.uid,
  });
  // @ts-ignore
  window.dataLayer.push({
    ...GA4Event,
    user_id: user.value?.uid,
  });
};

const sendEvent = (event: AnalyticsEvent) => {
  const { kind, data } = event;
  const { action, ...rest } = data as any;
  sendGA4Event({
    event: kind,
    event_name: `${kind}:${action}`,
    data: rest,
  });
};

const sendPlayerEvent = (event: PlayerEvent) => {
  const { state, ...rest } = event as any;
  sendGA4Event({
    event: "player",
    event_name: `player:${state}`,
    data: rest,
  });
};

const sendRawEvent = (event: AnalyticsEvent) => {
  const { kind, data } = event;
  sendGA4Event({
    event: kind,
    ...data,
  });
};

export { sendEvent, sendPlayerEvent, sendRawEvent };

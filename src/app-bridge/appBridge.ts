import log from "loglevel";
import { useIntervalFn } from "@vueuse/core";
import { useDevice } from "@/composables/device";
import { usePlayerStore } from "@/stores/player";
import { useQueueStore } from "@/stores/queue";

const HEARTBEAT_INTERVAL = 5000;

// for channel options see:
// obr-app/obrapp/modules/OBRWebView.swift
type channel =
  | "global:init"
  | "heartbeat"
  // queue
  | "queue:replace"
  | "queue:clear"
  | "queue:state"
  | "queue:update"
  // player
  | "player:playLive"
  | "player:playOnDemand"
  | "player:state"
  | "player:update";

type Message = {
  c: channel;
  d?: string;
};

type ReceivedEventDetail = {
  c: channel;
  d?: string;
};

type ReceivedEvent = Event & {
  detail?: ReceivedEventDetail;
};

class AppBridge {
  constructor() {
    const { isWeb } = useDevice();
    if (isWeb) {
      log.debug("AppBridge - web mod detected: disable bridge");
      return;
    }
    log.debug("AppBridge - constructor");
    this.init().then(() => {
      log.debug("AppBridge - initialized");
    });
    useIntervalFn(
      async () => {
        await this.heartbeat();
      },
      HEARTBEAT_INTERVAL,
      { immediateCallback: true }
    );
    window.addEventListener("appBridge", this.onReceive.bind(this));
  }
  async init(): Promise<void> {
    log.debug("AppBridge - init?");
    await this.send("global:init");
  }
  async heartbeat(): Promise<void> {
    log.debug("AppBridge - heartbeat");
    await this.send("heartbeat");
  }
  // web > native - send payload to channel
  async send(channel: channel, data?: object) {
    log.debug("AppBridge - send", channel, data);
    const message: Message = {
      c: channel,
    };
    if (data) {
      message.d = JSON.stringify(data);
    }
    // @ts-ignore
    if (window.webkit) {
      log.debug("payload", message);
      try {
        // @ts-ignore
        await window.webkit.messageHandlers.appBridge?.postMessage(message);
      } catch (e: unknown) {
        // console.warn(channel, e);
      }
    }
  }
  // web < native - handle received data
  async onReceive(e: ReceivedEvent) {
    if (!e.detail) {
      return;
    }
    const message: Message = e.detail;
    const data = message.d ? JSON.parse(message.d) : null;
    const { c: channel } = message;
    log.debug("AppBridge - onReceive", channel, data);
    // const { c: channel, d } = e.detail;
    // const data = d ? JSON.parse(d) : null;
    // log.debug("AppBridge - onReceive", channel, data);
    if (channel === "player:update" && data) {
      const { setPlayerState, setAppPlayerData } = usePlayerStore();
      const playerState = {
        ...data,
        // set dummy values
        duration: 60,
        absPosition: 30,
        bandwidth: 12800,
      };
      await setPlayerState(playerState);
      console.debug("playerState", playerState);
      // debug only, set whole data to store
      await setAppPlayerData(data);
    }
    if (channel === "queue:update" && data) {
      const { setQueueData } = useQueueStore();
      await setQueueData(data);
    }
  }
}

export { AppBridge };

import Hls from "hls.js";
import log from "loglevel";
import { isEqual, round } from "lodash-es";

import { useQueueControls } from "@/composables/queue";
import { hlsBaseConfig } from "@/proto/player/hlsConfig";
import type { State as StorePlayerState } from "@/proto/stores/player";
import { usePlayerStore } from "@/proto/stores/player";
import settings from "@/settings";

import type { AudioAnalyser } from "./analyser";
import { createAudioAnalyser } from "./analyser";

const PROTECTED_MEDIA = "https://media.next.openbroadcast.ch/";

const hlsConfig = {
  ...hlsBaseConfig,
  debug: false,
  xhrSetup: (xhr: XMLHttpRequest, url: string) => {
    xhr.withCredentials = url.startsWith(PROTECTED_MEDIA);
  },
};

type Mode = "live" | "ondemand";
type PlayState = "stopped" | "buffering" | "playing" | "paused";

type CueFade = {
  cueIn: number;
  cueOut: number;
  fadeIn: number;
  fadeOut: number;
};

const getLiveUrl = (): string => {
  return "https://obr-stream-hls.hazelfire.com/live.m3u8";
  // return `${settings.STREAM_ENDPOINTS.hls}?${Date.now()}`;
};

const getOnDemandUrl = (uid: string): string => {
  return `${settings.MEDIA_ENDPOINTS.hls}${uid}/hls/manifest.m3u8`;
};

const getStepVolume = (start: number, end: number, time: number, reverse = false) => {
  const duration = end - start;
  const position = time - start;
  const vol = position / duration;
  const vol2 = reverse ? 1 - vol : vol;
  return round(Math.sin((vol2 * Math.PI) / 2), 3);
  // return vol ? Math.log(vol * 100) / Math.log(100) : 0;
};

class HlsPlayer {
  static instance: HlsPlayer;
  private audio: HTMLAudioElement;
  private hls: null | Hls;

  private mediaUid: null | string = null;

  public duration = 0;
  public currentTime = 0;

  public mode: Mode = "live";
  public playState: PlayState = "stopped";

  private cueIn = 0;
  private cueOut = 0;
  private fadeIn = 0;
  private fadeOut = 0;

  private volume = 1;
  public baseVolume = 1; // user-controllable volume

  // actions from pinia store / composables need to be mapped in the constructor
  // as they are not ready earlier
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  setPlayerState = async (state: StorePlayerState): Promise<void> => {};

  analyser: AudioAnalyser;

  private debugData = {};

  private constructor() {
    const audio = document.createElement("audio");

    const nativeHlsSupported = !!audio.canPlayType("application/vnd.apple.mpegurl");
    const hlsSupported = Hls.isSupported();

    log.debug("nativeHlsSupported", nativeHlsSupported);
    log.debug("hlsSupported", hlsSupported);

    const hls = nativeHlsSupported ? null : new Hls(hlsConfig);

    this.setupAudioEvents(audio);

    if (hls) {
      this.setupHlsEvents(hls);
      hls.attachMedia(audio);
    }

    this.audio = audio;
    this.hls = hls;

    this.setupStore();

    this.analyser = createAudioAnalyser(audio);

    setInterval(async () => {
      await this.syncStateToStore();
    }, 5000);

    setInterval(async () => {
      await this.syncDebugDataToStore();
    }, 1000);
  }

  public static getInstance(): HlsPlayer {
    if (!HlsPlayer.instance) {
      HlsPlayer.instance = new HlsPlayer();
    }
    return HlsPlayer.instance;
  }

  private setupAudioEvents(audio: HTMLAudioElement) {
    // audio.addEventListener("audioprocess", (e: Event) => log.debug("audioprocess", e))
    // audio.addEventListener("canplay", (e: Event) => log.debug("canplay", e))
    // audio.addEventListener("canplaythrough", (e: Event) => log.debug("canplaythrough", e))
    // audio.addEventListener("complete", (e: Event) => log.debug("complete", e))
    // audio.addEventListener("durationchange", (e: Event) => log.debug("durationchange", e))
    // audio.addEventListener("emptied", (e: Event) => log.debug("emptied", e))
    // audio.addEventListener("ended", (e: Event) => log.debug("ended", e))
    // audio.addEventListener("loadeddata", (e: Event) => log.debug("loadeddata", e))
    // audio.addEventListener("loadedmetadata", (e: Event) => log.debug("loadedmetadata", e))
    // audio.addEventListener("pause", (e: Event) => log.debug("pause", e))
    // audio.addEventListener("play", (e: Event) => log.debug("play", e))
    // audio.addEventListener("playing", (e: Event) => log.debug("playing", e))
    // audio.addEventListener("seeked", (e: Event) => log.debug("seeked", e))
    // audio.addEventListener("seeking", (e: Event) => log.debug("seeking", e))
    // audio.addEventListener("stalled", (e: Event) => log.debug("stalled", e))
    // audio.addEventListener("suspend", (e: Event) => log.debug("suspend", e))
    // audio.addEventListener("timeupdate", (e: Event) => log.debug("stalled", e))

    // map audio element events to "internal" states
    audio.addEventListener("waiting", () => this.setPlayState("buffering"));
    audio.addEventListener("playing", () => this.setPlayState("playing"));
    audio.addEventListener("pause", () => this.setPlayState("paused"));
    audio.addEventListener("emptied", () => this.setPlayState("paused"));
    audio.addEventListener("ended", () => this.setPlayState("stopped"));

    audio.onended = async (): Promise<void> => {
      console.debug("onended");
      await this.playNext();
    };

    audio.addEventListener("durationchange", () => {
      this.duration = audio.duration;
    });

    audio.addEventListener("timeupdate", async () => {
      // log.debug("timeupdate", e);
      this.currentTime = audio.currentTime;

      await this.syncStateToStore();
    });

    // handler for cue & fades
    audio.addEventListener("timeupdate", this.onTimeupdate.bind(this), false);
  }

  private setupHlsEvents(hls: Hls) {
    hls.on(Hls.Events.MEDIA_ATTACHED, () => {
      // this.attached = true;
      log.debug("audio attached to hls");
    });

    // hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
    //   log.debug(event, data.levels);
    // });

    hls.on(Hls.Events.ERROR, (event, data) => {
      log.debug(event, data);
    });
  }

  private setupStore(): void {
    // connections to pinia store actions
    log.debug("setupStore");
    const { setPlayerState } = usePlayerStore();
    this.setPlayerState = setPlayerState;
  }

  private setPlayState(playState: PlayState): void {
    // log.debug("player setPlayState:", playState);
    this.playState = playState;
    this.syncStateToStore().then(() => {});
  }

  private setCueFade(cueFade: CueFade): void {
    // log.debug("setCueFade", cueFade);
    this.cueIn = cueFade.cueIn;
    this.cueOut = cueFade.cueOut;
    this.fadeIn = cueFade.fadeIn;
    this.fadeOut = cueFade.fadeOut;
  }

  private resetCueFade(): void {
    // log.debug("resetCueFade");
    this.cueIn = 0;
    this.cueOut = 0;
    this.fadeIn = 0;
    this.fadeOut = 0;
  }

  /*
  set combined volume by given value and configured `baseVolume`
  note: to control the volume from "outside" use `setBaseVolume`
  */
  private setVolume(value = 1): void {
    this.volume = value;
    log.debug("setVolume", value);
    this.audio.volume = this.volume * this.baseVolume;
  }

  /*
  handle cue-points and fade volumes
  */
  private async onTimeupdate(): Promise<void> {
    if (this.mode === "live") {
      if (this.volume < 1) {
        this.setVolume(1);
      }
      return;
    }

    const time = this.currentTime;
    const startTime = this.cueIn;
    const endTime = this.duration - this.cueOut;
    const fadeInEndTime = this.fadeIn ? startTime + this.fadeIn : 0;
    const fadeOutStartTime = this.fadeOut ? endTime - this.fadeOut : endTime;

    // check if time is after cue-out point
    // if no cue-out is set this is handled by the audio `ended` event
    if (this.cueOut && time > endTime) {
      log.debug("endTime reached");
      await this.pause();
      await this.playNext();
    }

    if (fadeInEndTime && startTime < time && time < fadeInEndTime) {
      // check if fade-in should occur
      const stepVolume = getStepVolume(startTime, fadeInEndTime, time);
      log.debug("fade-in in progress", stepVolume);
      this.setVolume(stepVolume);
    } else if (fadeOutStartTime && endTime > time && time > fadeOutStartTime) {
      // check if fade-out should occur
      const stepVolume = getStepVolume(fadeOutStartTime, endTime, time, true);
      log.debug("fade-out in progress", stepVolume);
      this.setVolume(stepVolume);
    } else if (time <= startTime) {
      // ensure 0 volume in case play position is before cue-in
      log.info("time before start time");
      this.setVolume(0);
    } else if (this.volume < 1 && time > fadeInEndTime && time < fadeOutStartTime) {
      // ensure volume is set to max
      log.info("reset volume");
      this.setVolume(1);
    }
  }

  public async playLive(): Promise<void> {
    log.debug("playLive");
    // const url = `http://local.obr-next:3000/encoded/hls/manifest.m3u8`;
    // const url = "https://obr-stream-hls.hazelfire.com/live.m3u8"
    const url = getLiveUrl();
    this.setPlayState("buffering");
    this.mode = "live";
    this.mediaUid = null;

    if (this.hls) {
      await this.hls.loadSource(url);
    } else {
      console.debug("load source: native mode", url);
      this.audio.src = url;
    }
    this.resetCueFade();
    await this.audio.play();
  }

  public async playUid(uid: string, estimatedDuration?: number, cueFade?: CueFade): Promise<void> {
    // log.debug("playUid:", uid, cueFade);
    if (estimatedDuration !== undefined) {
      this.duration = estimatedDuration;
    }
    if (cueFade) {
      this.setCueFade(cueFade);
    } else {
      this.resetCueFade();
    }
    // const url = `http://local.obr-next:3000/encoded/${uid}/hls/manifest.m3u8`;
    const url = getOnDemandUrl(uid);
    this.mode = "ondemand";
    if (uid !== this.mediaUid || this.playState === "buffering") {
      this.setPlayState("buffering");
      if (this.fadeIn) {
        log.debug("fade in: set volume to 0");
        // this.audio.volume = 0;
        this.setVolume(0);
      }
      if (this.hls) {
        await this.hls.loadSource(url);
      } else {
        console.debug("load source: native mode", url);
        this.audio.src = url;
      }
      this.currentTime = this.cueIn;
      this.audio.currentTime = this.currentTime;
      log.debug("seek to:", this.currentTime);
    }
    this.mediaUid = uid;
    try {
      await this.audio.play();
    } catch (e) {
      log.warn("unable to play. try again in 1s", e);
      setTimeout(async () => {
        await this.audio.play();
      }, 1000);
    }
  }

  public async pause(): Promise<void> {
    log.debug("pause");
    await this.audio.pause();
    if (this.mode === "live") {
      if (this.hls) {
        this.hls.stopLoad();
      } else {
        this.audio.src = "";
      }
    }
    // this.setPlayState("paused");
  }

  public async resume(): Promise<void> {
    log.debug("resume");
    if (this.mode === "live") {
      await this.playLive();
    } else {
      await this.audio.play();
    }
  }

  public async seek(p: number): Promise<void> {
    if (this.mode === "live") {
      log.debug("seek disabled in live mode");
      return;
    }
    log.debug("seek", p);
    const time = this.duration * p;
    this.audio.currentTime = Math.max(time, this.cueIn);
    await this.audio.play();
  }

  public setBaseVolume(value: number): void {
    this.baseVolume = value;
  }

  private async playNext(): Promise<void> {
    console.debug("play next");
    const { playNext } = useQueueControls();
    await playNext();
  }

  private async syncStateToStore(): Promise<void> {
    const { mode, playState, duration, currentTime, hls } = this;

    const state = {
      mode,
      playState,
      duration: duration === Infinity ? 0 : duration,
      currentTime,
      //
      liveLatency: round(hls?.latency ?? -1, 0),
      bandwidth: round(hls?.bandwidthEstimate ?? -1, 0),
    };
    await this.setPlayerState(state);
  }

  private async syncDebugDataToStore(): Promise<void> {
    if (!this.hls) {
      return;
    }

    const { hls, mode } = this;

    const { currentLevel, maxAutoLevel, bandwidthEstimate, latency, drift, mainForwardBufferInfo } =
      hls;

    const data = {
      mode,
      currentLevel,
      maxAutoLevel,
      bandwidthEstimate,
      latency,
      drift,
      mainForwardBufferInfo,
    };

    if (!isEqual(data, this.debugData)) {
      const { setPlayerDebugData } = usePlayerStore();
      await setPlayerDebugData(data);
    }
    this.debugData = data;
  }
}

export type { CueFade, Mode, PlayState };
export { HlsPlayer };

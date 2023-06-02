import { reactive, ref } from "vue";
import Hls from "hls.js";
import log from "loglevel";

const hlsConfig = {
  debug: false,
  maxBufferLength: 30,
  maxMaxBufferLength: 30,
  backBufferLength: 30,
  liveDurationInfinity: true,
  //
  xhrSetup: (xhr, url) => {
    log.debug(url, xhr);
    // xhr.withCredentials = true;
  },
};

type PlayMode = "live" | "ondemand";
type PlayState = "stopped" | "buffering" | "playing" | "paused";

class HlsPlayer extends EventTarget {
  static instance: HlsPlayer;
  private audio: HTMLAudioElement;
  private hls: Hls;

  private mediaUid: null | string = null;

  duration = 0;
  position = 0;

  playMode: PlayMode = "live";
  playState: PlayState = "stopped";

  s = reactive({
    duration: 0,
    currentTime: 0,
    position: 0,
  });

  // attached = false;

  private constructor() {
    super();

    const audio = document.createElement("audio");
    const hls = new Hls(hlsConfig);

    this.setupAudioEvents(audio);
    this.setupHlsEvents(hls);

    hls.attachMedia(audio);

    this.audio = audio;
    this.hls = hls;
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

    audio.addEventListener("durationchange", (e: Event) => {
      log.debug("durationchange", e);
      this.duration = audio.duration;
      this.s.duration = audio.duration;
    });

    audio.addEventListener("timeupdate", (e: Event) => {
      log.debug("timeupdate", e);
      this.s.currentTime = audio.currentTime;
      this.s.position = audio.currentTime / audio.duration;
    });
  }

  private setupHlsEvents(hls: Hls) {
    hls.on(Hls.Events.MEDIA_ATTACHED, () => {
      // this.attached = true;
      log.debug("audio attached to hls");
    });

    hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
      log.debug(event, data.levels);
    });

    hls.on(Hls.Events.ERROR, (event, data) => {
      log.debug(event, data);
    });
  }

  private onStateChange: Event = new Event("statechange");

  private setPlayState(playState: PlayState): void {
    log.debug("player setPlayState:", playState);
    this.playState = playState;
    this.dispatchEvent(this.onStateChange);
  }

  public static getInstance(): HlsPlayer {
    if (!HlsPlayer.instance) {
      HlsPlayer.instance = new HlsPlayer();
    }
    return HlsPlayer.instance;
  }

  public async playLive(): Promise<void> {
    log.debug("playLive");
    const url = `http://local.obr-next:3000/encoded/${uid}/hls/manifest.m3u8`;
    await this.hls.loadSource(url);
    await this.audio.play();
    this.playMode = "live";
    this.mediaUid = null;
  }

  public async playByUid(uid: string): Promise<void> {
    log.debug("playByUid:", uid);
    const url = `http://local.obr-next:3000/encoded/${uid}/hls/manifest.m3u8`;
    if (uid !== this.mediaUid) {
      await this.hls.loadSource(url);
    }
    await this.audio.play();
    this.playMode = "ondemand";
    this.mediaUid = uid;
  }

  public async pause(): Promise<void> {
    log.debug("pause");
    await this.audio.pause();
    this.setPlayState("paused");
  }
}

const player = HlsPlayer.getInstance();

window.hlsplayer = player;

const usePlayer = () => {
  const playState = ref<PlayState>("stopped");

  player.addEventListener("statechange", (e: Event) => {
    log.debug("statechange event", e);
    playState.value = player.playState;
  });

  const playByUid = (uid: string) => player.playByUid(uid);
  const pause = () => player.pause();

  return {
    playState,
    s: player.s,
    playByUid,
    pause,
  };
};

export { usePlayer };

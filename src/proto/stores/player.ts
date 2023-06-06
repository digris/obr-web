import log from "loglevel";
import { defineStore } from "pinia";
import { round } from "lodash-es";

import type { Mode, PlayState } from "@/proto/player/hlsPlayer";

export interface State {
  mode: Mode;
  playState: PlayState;
  duration: number;
  currentTime: number;
  bandwidth: number;
  liveLatency: number;
  //
  debugData?: object;
}

export const useHlsPlayerStore = defineStore("hlsPlayer", {
  state: (): State => ({
    mode: "live",
    playState: "stopped",
    duration: 0,
    currentTime: 0,
    bandwidth: 0,
    liveLatency: 24, // TODO: evaluate default latency
    //
    debugData: {},
  }),
  getters: {
    // mode mappers
    isLive(state: State): boolean {
      return state.mode === "live";
    },
    isOndemand(state: State): boolean {
      return state.mode === "ondemand";
    },
    // state mappers
    isPlaying(state: State): boolean {
      return state.playState === "playing";
    },
    isBuffering(state: State): boolean {
      return state.playState === "buffering";
    },
    isPaused(state: State): boolean {
      return state.playState === "paused";
    },
    // derived state
    relPosition(state: State): number {
      if (state.mode === "live") {
        return 0;
      }
      return state.currentTime / state.duration ? round(state.currentTime / state.duration, 4) : 0;
    },
  },
  actions: {
    async setPlayerState(state: State): Promise<void> {
      if (state.mode !== this.mode) {
        log.debug("hlsPlayerStore - update mode", state.mode);
        this.mode = state.mode;
      }
      if (state.playState !== this.playState) {
        log.debug("hlsPlayerStore - update playState", state.playState);
        this.playState = state.playState;
      }
      if (state.duration !== this.duration) {
        log.debug("hlsPlayerStore - update duration", state.duration);
        this.duration = state.duration;
      }
      if (state.currentTime !== this.currentTime) {
        if (state.mode === "live" && state.currentTime !== 0) {
          this.currentTime = 0;
        } else {
          // log.debug("hlsPlayerStore - update currentTime", state.currentTime);
          this.currentTime = state.currentTime;
        }
      }
      if (state.mode === "live" && state.liveLatency && state.liveLatency !== this.liveLatency) {
        this.liveLatency = state.liveLatency;
      }
      if (state.bandwidth !== this.bandwidth) {
        this.bandwidth = state.bandwidth;
      }
    },
    async setPlayerDebugData(data: object): Promise<void> {
      this.debugData = data;
    },
  },
});

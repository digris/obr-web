import { defineStore } from "pinia";
import { round } from "lodash-es";

import type { Mode, PlayState } from "@/player/hlsPlayer";

export interface State {
  mode: Mode;
  playState: PlayState;
  duration: number;
  currentTime: number;
  bandwidth: number;
  liveLatency: number;
}

interface PlayerState extends State {
  isVisible: boolean;
  debugData: object;
}

export const usePlayerStore = defineStore("player", {
  state: (): PlayerState => ({
    mode: "live",
    playState: "stopped",
    duration: 0,
    currentTime: 0,
    bandwidth: 0,
    liveLatency: 24, // TODO: evaluate default latency
    //
    isVisible: false,
    debugData: {},
  }),
  persist: {
    afterRestore: (ctx) => {
      console.log(`just restored '${ctx.store.$id}'`);
      console.debug((ctx.store.$state.playState = "paused"));
    },
    paths: ["isVisible"],
  },
  getters: {
    // mode mappers
    isLive(state: PlayerState): boolean {
      return state.mode === "live";
    },
    isOndemand(state: PlayerState): boolean {
      return state.mode === "ondemand";
    },
    // state mappers
    isPlaying(state: PlayerState): boolean {
      return state.playState === "playing";
    },
    isBuffering(state: PlayerState): boolean {
      return state.playState === "buffering";
    },
    isPaused(state: PlayerState): boolean {
      return state.playState === "paused";
    },
    // derived state
    relPosition(state: PlayerState): number {
      if (state.mode === "live") {
        return 0;
      }
      return state.currentTime / state.duration ? round(state.currentTime / state.duration, 4) : 0;
    },
  },
  actions: {
    setVisibility(visible: boolean): void {
      this.isVisible = visible;
    },
    async setPlayerState(state: State): Promise<void> {
      if (state.mode !== this.mode) {
        this.mode = state.mode;
      }
      if (state.playState !== this.playState) {
        this.playState = state.playState;
      }
      if (state.duration !== this.duration) {
        this.duration = state.duration;
      }
      if (state.currentTime !== this.currentTime) {
        if (state.mode === "live" && state.currentTime !== 0) {
          this.currentTime = 0;
        } else {
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

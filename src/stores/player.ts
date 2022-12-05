import { defineStore } from "pinia";
import { round } from "lodash-es";

type mode = "live" | "ondemand"; // NOTE: unify to "onDemand" (obr-app)
type state = "stopped" | "playing" | "paused" | "buffering";

export interface PlayerState {
  mode: mode;
  state: state;
  duration: number | null;
  absPosition: number | null;
  bandwidth: number;
}

interface State {
  // NOTE: temporary, debugging bridge
  appPlayerData: any;
  mode: mode;
  state: state;
  duration: number | null;
  absPosition: number | null;
  bandwidth: number;
  liveLatency: number;
}

export const usePlayerStore = defineStore("player", {
  state: (): State => ({
    appPlayerData: {},
    mode: "live",
    state: "stopped",
    duration: null,
    absPosition: null,
    bandwidth: 0,
    // effective playback latency, in seconds
    liveLatency: 0, // TODO: evaluate default latency
  }),
  getters: {
    // mode
    isLive(state: State): boolean {
      return state.mode === "live";
    },
    isOndemand(): boolean {
      return !this.isLive;
    },
    // state
    isPlaying(state: State): boolean {
      return state.state === "playing";
    },
    isBuffering(state: State): boolean {
      return state.state === "buffering";
    },
    isPaused(state: State): boolean {
      return state.state === "paused";
    },
    // progress / time
    relPosition(state: State): number | null {
      if (state.duration && state.absPosition) {
        return round(state.absPosition / state.duration, 4);
      }
      return null;
    },
  },
  actions: {
    async setPlayerState(playerState: PlayerState): Promise<void> {
      this.mode = playerState.mode;
      this.state = playerState.state;
      this.duration = playerState.duration;
      this.absPosition = playerState.absPosition;
      this.bandwidth = playerState.bandwidth;
    },
    async setLiveLatency(latency: number): Promise<void> {
      this.liveLatency = latency;
    },
    async setAppPlayerData(data: any) {
      this.appPlayerData = data;
    },
  },
});

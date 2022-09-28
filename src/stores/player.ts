import { defineStore } from "pinia";

// TODO: type definitions
interface State {
  configuration: any;
  bufferInfo: any;
  currentState: any;
  playerState: any;
}

export const usePlayerStore = defineStore("player", {
  state: (): State => ({
    configuration: {},
    bufferInfo: {},
    currentState: null,
    playerState: null,
  }),
  getters: {
    // playheadTime(state: State): DateTime | null {
    //   const time = state.playerState?.playheadTime;
    //   return time ? DateTime.fromJSDate(time) : null;
    // },
  },
  actions: {
    updatePlayerState(playerState: any) {
      this.playerState = playerState;
    },
  },
});

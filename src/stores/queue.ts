import type { Media } from "@/typings/api";
import { defineStore } from "pinia";
import { shuffle } from "lodash-es";

export type AnnotatedMedia = Media & {
  scope: Array<string>;
};

export interface Enqueue {
  media: Array<AnnotatedMedia>;
  mode?: string;
}

export interface State {
  media: Array<AnnotatedMedia>;
  currentIndex: number;
}

export const useQueueStore = defineStore("queue", {
  state: (): State => ({
    media: [],
    currentIndex: -1,
  }),
  getters: {
    numMedia(state: State): number {
      return state.media.length;
    },
    previousIndex(state: State): number | null {
      if (state.media[state.currentIndex - 1]) {
        return state.currentIndex - 1;
      }
      return null;
    },
    nextIndex(state: State): number | null {
      if (state.media[state.currentIndex + 1]) {
        return state.currentIndex + 1;
      }
      return null;
    },
    currentMedia(state: State): AnnotatedMedia | null {
      return state.media[state.currentIndex] || null;
    },
  },
  actions: {
    async setIndex(index: number): Promise<void> {
      console.debug("stores/queue - setIndex", index);
      this.currentIndex = index;
    },
    async removeAtIndex(index: number): Promise<void> {
      console.debug("stores/queue - removeIndex", index);
      this.media.splice(index, 1);
      if (index < this.currentIndex) {
        this.currentIndex -= 1;
      }
    },
    async enqueue(queue: Enqueue): Promise<void> {
      const { media, mode } = queue;
      console.debug("stores/queue - enqueue", media, mode);
      if (mode === "replace") {
        this.media = media;
        this.currentIndex = media.length ? 0 : -1;
      } else if (mode === "insert") {
        const splitAt = this.currentIndex + 1;
        const head = this.media.slice(0, splitAt);
        const tail = this.media.slice(splitAt);
        this.media = [...head, ...media, ...tail];
        if (this.currentIndex < 0) {
          this.currentIndex = media.length ? 0 : -1;
        }
      } else if (mode === "append") {
        this.media = [...this.media, ...media];
        if (this.currentIndex < 0) {
          this.currentIndex = media.length ? 0 : -1;
        }
      } else {
        console.warn(`unknown mode ${mode}`);
      }
    },
    async shuffleQueue(): Promise<void> {
      console.debug("stores/queue - shuffleQueue");
      const splitAt = this.currentIndex + 1;
      const head = this.media.slice(0, splitAt);
      const tail = this.media.slice(splitAt);
      this.media = [...head, ...shuffle(tail)];
    },
    async clearQueue(): Promise<void> {
      console.debug("stores/queue - clearQueue");
      this.media = this.media.slice(this.currentIndex, this.currentIndex + 1);
      this.currentIndex = 0;
    },
  },
});
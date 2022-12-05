import log from "loglevel";
import { defineStore } from "pinia";
import { shuffle } from "lodash-es";

import type { Media } from "@/typings/api";

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
    nextMedia(state: State): AnnotatedMedia | null {
      if (this.nextIndex) {
        return state.media[this.nextIndex] || null;
      }
      return null;
    },
  },
  actions: {
    async setIndex(index: number): Promise<void> {
      log.debug("queueStore - setIndex", index);
      this.currentIndex = index;
    },
    async deleteAtIndex(index: number): Promise<void> {
      log.debug("queueStore - removeIndex", index);
      this.media.splice(index, 1);
      if (index < this.currentIndex) {
        this.currentIndex -= 1;
      }
    },
    async enqueue(queue: Enqueue): Promise<void> {
      const { media, mode } = queue;
      log.debug("queueStore - enqueue", media, mode);
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
        log.warn(`unknown mode ${mode}`);
      }
    },
    async shuffleQueue(): Promise<void> {
      log.debug("queueStore - shuffleQueue");
      const splitAt = this.currentIndex + 1;
      const head = this.media.slice(0, splitAt);
      const tail = this.media.slice(splitAt);
      this.media = [...head, ...shuffle(tail)];
    },
    async clearQueue(): Promise<void> {
      log.debug("queueStore - clearQueue");
      this.media = this.media.slice(this.currentIndex, this.currentIndex + 1);
      this.currentIndex = 0;
    },
    // replace complete queue state
    // this method is used when running in "App-mode" and queue data is handled by native app
    async setQueueData(data: any): Promise<void> {
      log.debug("setQueueData", data);
      const { media, currentIndex } = data;
      this.media = media;
      this.currentIndex = currentIndex;
    },
  },
});

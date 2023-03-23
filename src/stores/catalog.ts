import { defineStore } from "pinia";

// import { without } from "lodash-es";
import {
  getArtist,
  getArtists,
  getMediaDetail,
  getMood,
  getMoods,
  getPlaylist,
} from "@/api/catalog";
import type { Artist, Media, Mood } from "@/typings/api";

interface State {
  artists: Array<Artist>;
  media: Array<Media>;
  moods: Array<Mood>;
  // NOTE: add type for playlist
  playlists: Array<any>;
}

interface ListLoadResult {
  count: number;
  next: string | null;
  results: Array<Artist | Media>;
}

export const useCatalogStore = defineStore("catalog", {
  state: (): State => ({
    artists: [],
    media: [],
    moods: [],
    playlists: [],
  }),
  getters: {
    artistByUid: (state: State) => (uid: string) => {
      return state.artists.find((obj) => obj.uid === uid) || null;
    },
    mediaByUid: (state: State) => (uid: string) => {
      return state.media.find((obj) => obj.uid === uid) || null;
    },
    moodByUid: (state: State) => (uid: string) => {
      return state.moods.find((obj) => obj.uid === uid) || null;
    },
    playlistByUid: (state: State) => (uid: string) => {
      return state.playlists.find((obj) => obj.uid === uid) || null;
    },
  },
  actions: {
    // async loadArtist(uid: string): Promise<void> {
    //   if (this.artistByUid(uid)) {
    //     console.debug(`already loaded: ${uid}`);
    //     return;
    //   }
    //   const objKey = `artist-${uid}`;
    //   if (this.loading.includes(objKey)) {
    //     console.debug(`already loading: ${objKey}`);
    //     return;
    //   }
    //   this.loading.push(objKey);
    //   this.artists.push(await getArtist(uid));
    //   this.loading = without(this.loading, objKey);
    // },
    async loadArtists(
      limit = 16,
      offset = 0,
      filter = {},
      ordering = [],
      reset = false
    ): Promise<ListLoadResult> {
      if (reset) {
        this.artists = [];
      }

      const { count, next, results } = await getArtists(limit, offset, filter, ordering);

      this.artists.push(...results);

      // const hasNext = !!next;
      // const numResults = count;

      return {
        count,
        next,
        results,
      };
    },
    async loadArtist(uid: string): Promise<void> {
      const artist = await getArtist(uid);
      const index = this.artists.findIndex((obj) => obj.uid === uid);
      if (index > -1) {
        this.artists[index] = artist;
      } else {
        this.artists.push(artist);
      }
      // if (!this.artistByUid(uid)) {
      //   this.artists.push(await getArtist(uid));
      // }
    },
    async loadMedia(uid: string): Promise<void> {
      if (!this.mediaByUid(uid)) {
        this.media.push(await getMediaDetail(uid));
      }
    },
    async loadPlaylist(uid: string): Promise<void> {
      if (!this.playlistByUid(uid)) {
        this.playlists.push(await getPlaylist(uid));
      }
    },
    async loadMood(uid: string): Promise<void> {
      if (!this.moodByUid(uid)) {
        this.moods.push(await getMood(uid));
      }
    },
    async loadMoods(): Promise<void> {
      const { results } = await getMoods(100, 0);
      this.moods = results;
    },
  },
});
